# Contenido del sitio

Todo lo que se publica en **Proyectos** y **Guías** sale de esta carpeta. Cada página es un archivo `.md` con un encabezado YAML entre dos líneas `---` y el texto en Markdown debajo. El nombre del archivo es la dirección: `guias/videos-a-60-fps-con-ffmpeg.md` → `tutiendita-ia.store/guias/videos-a-60-fps-con-ffmpeg/`.

Antes de subir un cambio, corré `python manage.py validar_contenido`: si falta un campo o hay un error, dice en qué archivo y qué corregir. El deploy también lo corre y no publica si falla.

## Proyecto (`proyectos/<nombre>.md`)

```yaml
---
nombre: Transcriptor Local                 # obligatorio
categoria: escritorio                      # escritorio | servicios | institucional
estado: produccion                         # produccion | desarrollo | piloto
etiqueta: whisper + pyannote               # la nota escrita a mano de la tarjeta (corta)
resumen: Una o dos frases.                 # obligatorio: se ve en la tarjeta y en Google
stack: [Python, faster-whisper]            # obligatorio
orden: 20                                  # opcional: menor = aparece antes
destacado: true                            # opcional: aparece en el inicio
version: "1.0"                             # opcional (entre comillas)
plataforma: Windows 10 / 11 (64 bits)      # opcional
repo: https://github.com/...               # opcional. En "escritorio" activa el botón de descarga (GitHub Releases)
web: https://...                           # opcional: botón "Visitar"
icono: img/proyectos/transcriptor_256.png  # opcional: ruta dentro de static/
datos:                                     # opcional: filas de la ficha técnica
  Modelo de voz: Whisper large-v3-turbo
---
## Qué es
...
```

## Guía (`guias/<nombre>.md`)

```yaml
---
titulo: Videos a 60 FPS con FFmpeg         # obligatorio
resumen: Una o dos frases.                 # obligatorio
proyecto: omniflow-fps-booster             # obligatorio: nombre de archivo de un proyecto
nivel: inicial                             # inicial | intermedio | avanzado
fecha: 2026-10-22                          # obligatorio, AAAA-MM-DD
actualizada: 2026-11-05                    # opcional
duracion: 30 minutos                       # opcional: tiempo de práctica
requisitos:                                # opcional: el recuadro "Antes de empezar"
  - FFmpeg instalado
borrador: true                             # opcional: no se publica mientras esté en true
---
## Paso 1: ...
```

Los títulos `##` y `###` arman el índice "En esta guía".

## Lo que se puede usar en el texto

- Tablas, listas, enlaces, `código` y bloques de código con lenguaje (```` ```python ````, ```` ```bash ````): se colorean solos.
- Recuadros de aviso:

```markdown
!!! warning "Título del aviso"
    Texto con cuatro espacios adelante.
```

(`note` para notas y `warning` para advertencias.)

## Reglas para las guías

- **Probá cada comando antes de publicarlo.** Si algo no se pudo probar (por ejemplo, algo que necesita una placa NVIDIA), decilo en el texto.
- Escribí lo que el código **hace hoy**, no lo que dice el README de la app (ver `docs/AUDITORIA-REPOS-2026-10-22.md`).
- Nada de claves, tokens ni datos de clientes en los ejemplos.
