"""Gunicorn para tutiendita-ia.store. Socket unix detrás de Nginx (deploy/nginx/tutiendita-ia.conf)."""

import os

bind = "unix:/run/tutiendita-ia/gunicorn.sock"
# El VPS es compartido (Campus del CFP, tienda, Ollama): la Etapa 1 es liviana y con 2 workers sobra.
workers = int(os.environ.get("GUNICORN_WORKERS", 2))
threads = 2
timeout = 30
graceful_timeout = 20
max_requests = 1000
max_requests_jitter = 100
accesslog = "-"
access_log_format = '%(h)s %(t)s "%(m)s %(U)s" %(s)s %(b)s %(L)s'
errorlog = "-"
loglevel = "info"
forwarded_allow_ips = "127.0.0.1"
