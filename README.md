# Tu Tiendita IA · Centro de Comando y Ecosistema Oficial

> **Sitio Web Oficial:** [tutiendita-ia.store](https://tutiendita-ia.store)  
> Factoría de software, herramientas para creadores, personalización con Inteligencia Artificial y desarrollos a medida.

---

## 🌟 Acerca de este Repositorio

Este repositorio actúa como el **meta-repositorio y centro de comando** de todo el ecosistema de **Tu Tiendita IA**. Integra la información técnica, catálogo de productos, identidad visual y especificaciones completas para el desarrollo del sitio web oficial en `tutiendita-ia.store`.

Contiene:
- **El sitio web** `tutiendita-ia.store` (Django): portfolio, guías paso a paso y, en las próximas etapas, el foro y el campus. Ver [Sitio web](#-sitio-web).
- **`CLAUDE.md`**: Guía maestra de contexto para trabajo asistido por IA (Claude Code, Claude Projects).
- **`CATALOGO_PRODUCTOS.json`**: Base de datos estructurada de todas las aplicaciones de escritorio, servicios de personalización con IA y proyectos institucionales.
- **`docs/`**: [hoja de ruta](docs/HOJA-DE-RUTA.md), [despliegue en el VPS](docs/DESPLIEGUE.md) y la [auditoría de los 12 repos](docs/AUDITORIA-REPOS-2026-10-22.md).
- Enlaces y referencias a los 12 repositorios oficiales en GitHub.

---

## 🚀 Repositorios del Ecosistema

### 🖥️ Suite de Software de Escritorio
- **[OmniSuite Studio](https://github.com/serranicolasp2-sudo/OmniSuite-Studio)**
- **[OmniBoost Studio](https://github.com/serranicolasp2-sudo/OmniBoost-Studio)**
- **[OmniFlow FPS Booster](https://github.com/serranicolasp2-sudo/OmniFlow-FPS-Booster)**
- **[OmniScale Studio](https://github.com/serranicolasp2-sudo/OmniScale-Studio)**
- **[Transcriptor Local](https://github.com/serranicolasp2-sudo/Transcriptor-Local)**

### 🛍️ E-Commerce & Servicios IA
- **[TuTiendita-Tienda](https://github.com/serranicolasp2-sudo/TuTiendita-Tienda)**
- **[TuTiendita-Centralita](https://github.com/serranicolasp2-sudo/TuTiendita-Centralita)**
- **[TuTiendita-Web](https://github.com/serranicolasp2-sudo/TuTiendita-Web)**
- **[TuTiendita-Produccion](https://github.com/serranicolasp2-sudo/TuTiendita-Produccion)**
- **[TuTiendita-Marca](https://github.com/serranicolasp2-sudo/TuTiendita-Marca)**

### 🎓 Proyectos Educativos
- **[CFP-401-Avellaneda](https://github.com/serranicolasp2-sudo/CFP-401-Avellaneda)**
- **[Campus-Virtual-Semi](https://github.com/serranicolasp2-sudo/Campus-Virtual-Semi)**

---

## 🌐 Identidad de Marca
- **Web Oficial:** [tutiendita-ia.store](https://tutiendita-ia.store)  
- **Titular:** Nicolás Serra

---

## 🖥️ Sitio web

Django 5.2 LTS, sin build de frontend. Los proyectos y las guías son archivos Markdown en [`contenido/`](contenido/LEEME.md).

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements/dev.txt
python manage.py runserver                            # http://localhost:8000
```

| Comando | Qué hace |
|---|---|
| `pytest` | Tests (páginas, contenido, sitemap, feed, seguridad) |
| `ruff check . && ruff format --check .` | Estilo |
| `python manage.py validar_contenido` | Revisa que todos los `.md` de `contenido/` estén bien |

| Carpeta | Contenido |
|---|---|
| `apps/core` | Inicio, sobre mí, foro y campus (próximamente), salud, robots |
| `apps/contenido` | Lector de Markdown, proyectos, guías, sitemap y RSS |
| `contenido/` | Las fichas de proyecto y las guías |
| `templates/`, `static/` | Plantillas, CSS y fuentes de la marca (servidas desde el propio dominio) |
| `deploy/` | Nginx, systemd, Gunicorn y `deploy.sh` para el VPS |

