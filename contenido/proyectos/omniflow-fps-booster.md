---
nombre: OmniFlow FPS Booster
categoria: escritorio
estado: produccion
version: "1.0"
orden: 40
etiqueta: 24 → 60 fps
resumen: Lleva videos de 24 o 30 FPS a 60 o 120 FPS generando cuadros intermedios, para paneos sin tirones.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, FFmpeg, CustomTkinter, PyInstaller]
repo: https://github.com/serranicolasp2-sudo/OmniFlow-FPS-Booster
incluido_en: omnisuite-studio
icono: img/proyectos/omniflow_256.png
datos:
  Destinos: 48, 50, 60 y 120 FPS
  Calidad: CRF 16, 18 o 20
  Aceleración: NVIDIA NVENC (H.264 / HEVC), AMD AMF o CPU
---

## Qué es

Los videos a 24 o 30 cuadros por segundo "tironean" en los paneos y en la acción rápida. OmniFlow genera cuadros nuevos entre los originales para que el movimiento se vea fluido a 60 FPS (o a 120, para cámara lenta).

Es especialmente útil con videos generados por IA, que casi siempre salen a 24 FPS.

## Los cinco métodos

Cada método de la app es un filtro distinto de FFmpeg, elegido según el tipo de material:

| Método | Filtro | Cuándo usarlo |
|---|---|---|
| Universal adaptativo | `framerate` con detección de cortes | Video real, 3D, cine |
| Anime y 2D | `framerate` con un umbral de corte más sensible | Animación con dibujos "a 2" o "a 3" |
| Motion Blend | `minterpolate` en modo `blend` | Paneos rápidos que tironean |
| Cadencia pura | `fps` | Duplicar cuadros sin inventar nada |
| Estimación de movimiento (MCI) | `minterpolate` con `mi_mode=mci` | Un plano clave donde la mezcla se nota. Calcula vectores de movimiento: es lento |

La detección de cortes (`scene`) es clave: evita que la herramienta mezcle el último cuadro de una escena con el primero de la siguiente.

Los cuatro primeros **mezclan** cuadros vecinos, que es rápido y nunca deforma la imagen. El quinto **calcula** dónde está cada parte de la imagen en el cuadro intermedio: con objetos rápidos se ve más natural, pero tarda mucho más y, con movimientos complejos (manos, pelo, agua), puede dejar zonas "derretidas".

Acepta `.mp4`, `.mov`, `.mkv`, `.avi`, `.webm`, `.flv`, `.ts`, `.m4v`, `.mpg`, `.mpeg` y `.wmv`, y procesa carpetas enteras.

## Paso a paso

La guía [Videos a 60 FPS con FFmpeg](/guias/videos-a-60-fps-con-ffmpeg/) explica cómo hacerlo desde la línea de comandos, con los mismos filtros que usa la app.
