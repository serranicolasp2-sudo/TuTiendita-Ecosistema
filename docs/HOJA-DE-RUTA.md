# Hoja de ruta de tutiendita-ia.store

**La idea:** una web personal con el portfolio de proyectos, un **foro abierto** con el paso a paso de cada uno (gratis, con bots que participan) y un **campus** con cursos pagos en video, guiados y con seguimiento personalizado.

**Regla del negocio:** el paso a paso es gratis y abierto; lo pago es el acompañamiento (video, recorrido ordenado, corrección y seguimiento).

---

## Etapa 1: portfolio y guías ✅ (este repo)

- Inicio, proyectos (11 fichas), guías paso a paso (2), sobre mí y las páginas de "próximamente" del foro y el campus.
- El contenido son archivos Markdown en `contenido/` (ver `contenido/LEEME.md`). Nada de panel de administración por ahora: se escribe, se sube a git y se publica con un deploy.
- Las apps de escritorio enlazan a **GitHub Releases** (`/releases/latest`). **Pendiente:** al 2026-10-22 ninguno de los 5 repos tiene releases publicadas, así que hay que subir los `.exe` y `.zip`.
- Sitemap, RSS de las guías, robots.txt y encabezados de seguridad (CSP estricta, todo servido desde el propio dominio, fuentes incluidas).
- Despliegue: `docs/DESPLIEGUE.md`.

**Para cerrar la etapa:** cargar el contacto (WhatsApp, Instagram, mail) en `/etc/tutiendita-ia/env`, publicar las releases y revisar el texto de "Sobre mí".

---

## Etapa 2: cuentas y foro abierto con bots

### Decisión: foro propio en Django (no Discourse)

Se evaluó Discourse (la mejor opción entre los foros existentes, con su plugin oficial *Discourse AI*, que ya sabe usar un modelo propio como Ollama). Se descartó por ahora, porque:

| | Discourse | Foro propio en Django |
|---|---|---|
| RAM | 2 a 4 GB solo para él (Docker, su Postgres, Redis, Sidekiq) | Lo que ya usa el sitio (~200 MB) |
| Cuentas | Un segundo sistema de login (se puede unificar con DiscourseConnect) | **Una sola cuenta** para el foro y el campus |
| Base | De cero | El Campus del Semi ya tiene `Foro`, `HiloForo`, `MensajeForo`, notificaciones y cola de mails |
| Bots | Plugin listo | Servicio propio (abajo) |

El VPS (6 núcleos, 12 GB, 100 GB NVMe) lo comparten el Campus del CFP, la tienda, la web Flask y Ollama. Con un foro propio queda margen para el modelo de los bots. **Si el foro crece mucho**, se puede migrar a Discourse en un VPS aparte; los hilos se exportan.

### Qué se construye

1. **Cuentas** con `django-allauth`: mail y Google, verificación de mail y recuperar clave (la misma configuración que el Campus).
2. **Pasar a PostgreSQL** (ya está en el VPS por el Campus; base y usuario propios).
3. **App `foro`**, adaptada de `Campus-Virtual-Semi/apps/comunicacion`:
    - categorías abiertas (video, audio, automatización, agentes, desarrollo con IA, "mostrá lo que armaste");
    - **un hilo por cada guía**, enlazado al pie de la guía;
    - moderación: reportes, ocultar mensajes, límite de mensajes por hora a las cuentas nuevas.
4. **Bots** (ver abajo).

### Bots con Ollama

- **Cómo corren:** un comando de Django (`manage.py bots`) que dispara un temporizador de systemd. No necesita un servidor web aparte. Le habla a Ollama por su API local (`http://127.0.0.1:11434`).
- **Modelo:** chico, de 3 a 4 mil millones de parámetros (por ejemplo `llama3.2:3b`, `qwen2.5:3b` o `gemma3:4b`), cuantizado. Usa unos 3 a 4 GB de RAM y en 6 núcleos genera algunas palabras por segundo: alcanza para un foro, donde una respuesta "en un rato" está bien. Antes de elegir hay que **medir la RAM libre** (`free -h`) con todo lo demás andando.
- **Siempre identificados:** cada bot es un usuario con una insignia **"Bot"** visible y una página que explica qué hace. Nunca se hacen pasar por personas.
- **Tres bots:**
    1. **Noticias:** una vez por día lee una lista fija de fuentes (RSS de blogs oficiales y medios de tecnología), publica un resumen corto con el **enlace a la fuente** y no copia notas enteras.
    2. **Ayudante:** cuando alguien lo menciona (`@ayudante`) o una pregunta queda 24 h sin respuesta, propone una respuesta usando las guías del sitio como contexto. Sus respuestas quedan marcadas como "respuesta automática, puede tener errores".
    3. **Debate:** abre un tema por semana a partir de las noticias.
- **Controles:** tope de mensajes por bot por día, cola de revisión opcional (Nicolás aprueba antes de publicar) y un botón para apagarlos sin hacer un deploy.

---

## Etapa 3: campus con cursos pagos

- **App `campus`:** cursos → módulos → lecciones (video, texto, archivos), avance por alumno, ejercicios con entrega y corrección (se reutiliza `apps/entregas` del Campus) y certificado al terminar.
- **Cobro:** Mercado Pago Checkout Pro, reutilizando lo que ya está probado en `TuTiendita-Tienda/app/mp.py` (firma del webhook, idempotencia, controlar que el pago corresponda al pedido). El pago confirmado habilita el curso.
- **Seguimiento personalizado:** mensajería alumno ↔ docente (`Conversacion` y `MensajeDirecto` del Campus) y turnos de consulta.
- **Video** (decisión pendiente):
    - *En el VPS:* Nginx sirve los archivos con `X-Accel-Redirect`, como hace el Campus con los PDF. Es gratis, pero consume disco (100 GB) y ancho de banda, y cualquier alumno puede descargar el video.
    - *En un servicio de video* (Bunny Stream, Vimeo): cuesta poco por mes, adapta la calidad a la conexión, tiene enlaces firmados y no carga el VPS. **Recomendado** cuando haya más de un par de cursos.

---

## Pendientes fuera del sitio

- **Desinstalar Moodle** sin romper la tienda ni el Campus: ver `docs/DESPLIEGUE.md` → "Antes de desinstalar Moodle".
- **Mudar la tienda** de `campuscfp401avellaneda.com.ar/tutienditaia/` a este dominio, actualizando antes las URLs en Mercado Pago.
- **Arreglos en las apps** detectados en `docs/AUDITORIA-REPOS-2026-10-22.md`, sobre todo el error de OmniBoost, que se cuelga en el primer video.
