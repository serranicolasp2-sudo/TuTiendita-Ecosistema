"""Producción en el VPS: detrás de Nginx con HTTPS (deploy/nginx/tutiendita-ia.conf)."""

from .base import *  # noqa: F403
from .base import env

DEBUG = False
SECRET_KEY = env("SECRET_KEY")  # sin default: si falta, no arranca
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
# HSTS: una semana para empezar; subir a un año (31536000) cuando el dominio esté estable.
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=604800)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
