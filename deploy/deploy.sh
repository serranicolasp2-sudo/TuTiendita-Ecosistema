#!/usr/bin/env bash
# Despliegue de una versión de tutiendita-ia.store. Mismo esquema que Campus-Virtual-Semi.
#   sudo -u tutiendita deploy/deploy.sh v0.1.0       # despliega el tag indicado
#   sudo -u tutiendita deploy/deploy.sh --rollback   # vuelve a la versión anterior
# Estructura: /srv/tutiendita-ia/{repo, releases/<tag>, actual -> releases/<tag>, anterior -> releases/<tag previo>, venv}
set -euo pipefail
BASE=/srv/tutiendita-ia
cd "$BASE"
set -a; [[ -f /etc/tutiendita-ia/env ]] && source /etc/tutiendita-ia/env; set +a

if [[ "${1:-}" == "--rollback" ]]; then
  [[ -L anterior ]] || { echo "No hay versión anterior"; exit 1; }
  destino=$(readlink -f anterior)
  ln -sfn "$(readlink -f actual)" anterior.tmp && ln -sfn "$destino" actual && mv -T anterior.tmp anterior
  # restart, NO reload: Gunicorn resolvió el enlace 'actual' al arrancar y con reload sigue el código viejo.
  sudo systemctl restart tutiendita-ia
  echo "Rollback a $(basename "$destino")."
  exit 0
fi

TAG="${1:?Indicá el tag a desplegar, p. ej. v0.1.0}"

echo "== 1/5 código $TAG"
git -C repo fetch --tags --quiet
if [[ ! -d "$BASE/releases/$TAG" ]]; then
  git -C repo worktree add "$BASE/releases/$TAG" "$TAG"
fi

echo "== 2/5 dependencias"
venv/bin/pip install --quiet -r "$BASE/releases/$TAG/requirements/prod.txt"

echo "== 3/5 chequeos, contenido, migraciones y estáticos"
cd "$BASE/releases/$TAG"
../../venv/bin/python manage.py check --deploy --fail-level ERROR
../../venv/bin/python manage.py validar_contenido
../../venv/bin/python manage.py migrate --noinput
../../venv/bin/python manage.py collectstatic --noinput --verbosity 0
cd "$BASE"

echo "== 4/5 cambio de versión"
[[ -L actual ]] && ln -sfn "$(readlink -f actual)" anterior
ln -sfn "$BASE/releases/$TAG" actual
sudo systemctl restart tutiendita-ia

echo "== 5/5 salud"
sleep 3
pid=$(systemctl show -p MainPID --value tutiendita-ia)
corriendo=$(sudo readlink -f "/proc/$pid/cwd")
[[ "$corriendo" == "$(readlink -f "$BASE/releases/$TAG")" ]] || { echo "ERROR: corre $corriendo, no $TAG"; exit 1; }
# Host real (ALLOWED_HOSTS no incluye localhost) y X-Forwarded-Proto https (si no, SECURE_SSL_REDIRECT responde 301).
curl -fsS --unix-socket /run/tutiendita-ia/gunicorn.sock -H "X-Forwarded-Proto: https" "http://${ALLOWED_HOSTS%%,*}/salud/" | grep -q '"status": "ok"' && echo " OK: $TAG desplegado"
