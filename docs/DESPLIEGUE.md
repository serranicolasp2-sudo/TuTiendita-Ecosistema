# Despliegue de tutiendita-ia.store en el VPS

El sitio se instala **al lado** de lo que ya corre en el VPS (Campus del CFP, la tienda y la web Flask), con su propio usuario, su propio servicio y su propio bloque de Nginx. No modifica la configuración de nada existente.

| Qué | Dónde |
|---|---|
| Código | `/srv/tutiendita-ia/{repo, releases/<tag>, actual → releases/<tag>, venv}` |
| Variables y claves | `/etc/tutiendita-ia/env` (600, dueño `tutiendita`) |
| Datos (base SQLite de la Etapa 1) | `/var/lib/tutiendita-ia/` |
| Servicio | `tutiendita-ia.service` (Gunicorn en `/run/tutiendita-ia/gunicorn.sock`) |
| Nginx | `/etc/nginx/sites-available/tutiendita-ia` |

Los archivos de configuración están en `deploy/`. Se probaron en Ubuntu con Nginx 1.24, HTTP/2 y Gunicorn por socket.

---

## 0. DNS (en el panel donde compraste el dominio)

Creá dos registros **A** con la IP pública del VPS:

| Tipo | Nombre | Valor |
|---|---|---|
| A | `@` (o `tutiendita-ia.store`) | IP del VPS |
| A | `www` | IP del VPS |

Si el VPS tiene IPv6, sumá los mismos registros como **AAAA**. Para comprobar (puede tardar desde minutos hasta unas horas):

```bash
dig +short tutiendita-ia.store
dig +short www.tutiendita-ia.store
```

Las dos tienen que devolver la IP del VPS **antes** del paso 5.

## 1. Usuario, carpetas y código

```bash
sudo apt install -y python3-venv git
sudo adduser --system --group --home /srv/tutiendita-ia --shell /usr/sbin/nologin tutiendita
sudo mkdir -p /srv/tutiendita-ia/releases /var/lib/tutiendita-ia /etc/tutiendita-ia
sudo chown -R tutiendita:tutiendita /srv/tutiendita-ia /var/lib/tutiendita-ia
sudo -u tutiendita git clone https://github.com/serranicolasp2-sudo/TuTiendita-Ecosistema.git /srv/tutiendita-ia/repo
sudo -u tutiendita python3 -m venv /srv/tutiendita-ia/venv
```

## 2. Variables de entorno

```bash
sudo cp /srv/tutiendita-ia/repo/deploy/env.prod.example /etc/tutiendita-ia/env
sudo chown tutiendita:tutiendita /etc/tutiendita-ia/env
sudo chmod 600 /etc/tutiendita-ia/env
python3 -c "import secrets; print(secrets.token_urlsafe(50))"   # copiá el resultado en SECRET_KEY
sudo nano /etc/tutiendita-ia/env
```

Completá `SECRET_KEY` y, si querés que aparezcan en el sitio, `CONTACTO_WHATSAPP` (solo dígitos, con 549), `CONTACTO_INSTAGRAM` y `CONTACTO_EMAIL`. Los que queden vacíos no se muestran.

> Si editás el archivo desde Windows, sacale los finales de línea de Windows (`sudo sed -i 's/\r$//' /etc/tutiendita-ia/env`). Es el mismo problema que ya pasó con la tienda.

## 3. Permisos para reiniciar el servicio

`deploy.sh` corre como `tutiendita` y necesita reiniciar su propio servicio, y nada más:

```bash
echo 'tutiendita ALL=(root) NOPASSWD: /usr/bin/systemctl restart tutiendita-ia, /usr/bin/readlink -f /proc/*/cwd' | sudo tee /etc/sudoers.d/tutiendita-ia
sudo chmod 440 /etc/sudoers.d/tutiendita-ia
sudo visudo -cf /etc/sudoers.d/tutiendita-ia     # tiene que decir "parsed OK"
```

## 4. Servicio y primer despliegue

El despliegue trabaja con **tags** de git. Una vez que el código esté en `main`, se crea el tag de la versión, por ejemplo `v0.1.0`, desde GitHub (Releases → *Draft a new release*) o con `git tag v0.1.0 && git push --tags`.

```bash
sudo cp /srv/tutiendita-ia/repo/deploy/systemd/tutiendita-ia.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tutiendita-ia
sudo -u tutiendita /srv/tutiendita-ia/repo/deploy/deploy.sh v0.1.0
```

El script baja el tag, instala las dependencias, valida el contenido (`validar_contenido`), corre los chequeos de seguridad de Django, junta los estáticos, cambia la versión y confirma que responde. Si algo falla, **no cambia la versión que está andando**.

## 5. Certificado HTTPS

Con el DNS ya apuntando al VPS:

```bash
sudo certbot certonly --nginx -d tutiendita-ia.store -d www.tutiendita-ia.store
```

Se usa `certonly` porque el archivo de Nginx del paso siguiente ya trae las rutas del certificado: si se instalara antes de tenerlo, `nginx -t` fallaría. La renovación automática la hace el temporizador de certbot que ya está instalado en el VPS.

## 6. Nginx

```bash
sudo cp /srv/tutiendita-ia/repo/deploy/nginx/tutiendita-ia.conf /etc/nginx/sites-available/tutiendita-ia
sudo ln -s /etc/nginx/sites-available/tutiendita-ia /etc/nginx/sites-enabled/tutiendita-ia
sudo nginx -t && sudo systemctl reload nginx
```

## 7. Verificación

```bash
curl -I http://tutiendita-ia.store/           # 301 a https://tutiendita-ia.store/
curl -I https://www.tutiendita-ia.store/      # 301 a https://tutiendita-ia.store/
curl -s https://tutiendita-ia.store/salud/    # {"status": "ok", "proyectos": 11, "guias": 2}
journalctl -u tutiendita-ia -n 50             # sin errores
```

Abrí el sitio desde el celular con datos móviles (no con el wifi de casa) para confirmar que se ve desde afuera.

---

## Publicar una versión nueva

1. Subí los cambios a `main` (contenido nuevo, guías, código).
2. Creá el tag de la versión (`v0.1.1`, `v0.2.0`…).
3. En el VPS: `sudo -u tutiendita /srv/tutiendita-ia/actual/deploy/deploy.sh v0.1.1`

**Para volver atrás:** `sudo -u tutiendita /srv/tutiendita-ia/actual/deploy/deploy.sh --rollback`

> Se puede editar un `.md` directamente en `/srv/tutiendita-ia/actual/contenido/` y el cambio se ve al instante. Pero se pierde en el próximo despliegue: lo correcto es hacerlo en git.

---

## ⚠️ Antes de desinstalar Moodle

Según `TuTiendita-Tienda/deploy/INSTALAR.md`, el bloque `server` de Nginx de **campuscfp401avellaneda.com.ar** (hoy en `/etc/nginx/sites-available/moodle`) **no es solo de Moodle**. Adentro también están:

- **la tienda**: `/tutienditaia/api/`, `/tutienditaia/revisar/` y las landings `/tutienditaia/…`. **Es la URL que figura en Mercado Pago**;
- según cómo se haya instalado, **el Campus del Semi** bajo `/semi/` (`Campus-Virtual-Semi/deploy/nginx/semi-locations.conf`).

Por eso, al sacar Moodle:

1. **Backup primero:** la base de datos de Moodle (`mysqldump` o `pg_dump`, según cuál use), la carpeta `moodledata` y una copia de `/etc/nginx/sites-available/moodle`.
2. **No borres ese archivo de Nginx.** Sacá solo las `location` de Moodle (las de `.php`, `/campus`, etc.) y dejá intactas las `^~ /tutienditaia/` y `^~ /semi/`, con el mismo `server_name` y el mismo certificado.
3. `sudo nginx -t && sudo systemctl reload nginx` y comprobá:
    - `curl -s https://campuscfp401avellaneda.com.ar/tutienditaia/api/salud`
    - el Campus en `/semi/`
4. Recién ahí: desinstalá PHP-FPM y la base de Moodle si nadie más las usa, y borrá `moodledata`.

Más adelante conviene mudar la tienda a este dominio (por ejemplo, `tutiendita-ia.store/tienda/`). Hay que hacerlo actualizando primero las URLs de retorno y del webhook en Mercado Pago. Queda en la hoja de ruta.

## Recursos del VPS

6 núcleos, 12 GB de RAM y 100 GB NVMe. La Etapa 1 usa unos 100 MB por worker de Gunicorn (2 workers). Para ver cómo queda la máquina antes de sumar el foro y los bots:

```bash
free -h
df -h /
systemctl list-units --type=service --state=running | grep -E "nginx|gunicorn|uvicorn|ollama|postgres|php|mysql|maria"
```
