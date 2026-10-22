"""Settings comunes a todos los entornos. Variables de entorno: deploy/env.prod.example."""

from pathlib import Path

import environ
from csp.constants import NONE, SELF

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    env.read_env(str(_env_file))

SECRET_KEY = env("SECRET_KEY", default="solo-para-desarrollo-no-usar-en-produccion")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])
SITE_URL = env("SITE_URL", default="http://localhost:8000")
TITULAR = "Nicolás Serra"

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "csp",
    "apps.core",
    "apps.contenido",
    # Etapa 2: auth, sessions, admin, allauth y apps.foro · Etapa 3: apps.campus (docs/HOJA-DE-RUTA.md)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "apps.core.context_processors.sitio",
            ],
        },
    },
]

# La Etapa 1 no guarda nada en la base (el contenido son archivos Markdown en contenido/).
# Queda configurada para que el foro y el campus solo tengan que sumar sus apps.
DATABASES = {"default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}

# Contenido del sitio: proyectos y guías en Markdown con encabezado YAML (ver contenido/LEEME.md)
CONTENIDO_DIR = Path(env("CONTENIDO_DIR", default=str(BASE_DIR / "contenido")))

# Datos de contacto públicos (Nicolás autorizó publicarlos). El env los puede cambiar; una línea vacía en
# /etc/tutiendita-ia/env no los borra gracias al "or".
CONTACTO = {
    "whatsapp": env("CONTACTO_WHATSAPP", default="") or "5491166912647",  # solo dígitos, con 54 9
    "whatsapp_visible": env("CONTACTO_WHATSAPP_VISIBLE", default="") or "11 6691-2647",
    "instagram": env("CONTACTO_INSTAGRAM", default="") or "_nicochapu",  # usuario sin @
    "email": env("CONTACTO_EMAIL", default="") or "serranicolas.p@gmail.com",
    "github": env("CONTACTO_GITHUB", default="") or "https://github.com/serranicolasp2-sudo",
}

# Seguridad común
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
# Todo se sirve desde el propio dominio (las fuentes también): la política puede ser estricta.
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": [SELF],
        "img-src": [SELF, "data:"],
        "script-src": [SELF],
        "style-src": [SELF],
        "font-src": [SELF],
        "object-src": [NONE],
        "base-uri": [SELF],
        "frame-ancestors": [NONE],
        "form-action": [SELF],
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"consola": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["consola"], "level": env("LOG_NIVEL", default="INFO")},
}
