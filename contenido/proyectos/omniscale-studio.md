---
nombre: OmniScale Studio
categoria: escritorio
estado: produccion
version: "1.0"
orden: 50
etiqueta: 1080p · 4K · 9:16
resumen: Escala videos a 1080p, 2K o 4K, horizontales o verticales, cuidando los bordes y las texturas.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, FFmpeg, CustomTkinter, PyInstaller]
repo: https://github.com/serranicolasp2-sudo/OmniScale-Studio
incluido_en: omnisuite-studio
icono: img/proyectos/omniscale_256.png
datos:
  Métodos: Lanczos + CAS, Spline36, Lanczos puro, Anime y Fílmico
  Formatos: 16:9, 9:16 (Reels / TikTok / Shorts) y 1:1
  Aceleración: NVIDIA NVENC, AMD AMF o CPU
---

## Qué es

Un escalador de video para cuando el material es chico (480p, 720p) y tiene que verse bien en una pantalla grande o en un reel vertical.

## Cómo escala

El método recomendado combina dos pasos de FFmpeg:

1. **Lanczos** con `accurate_rnd` y `full_chroma_int` para remuestrear con la mejor precisión de color.
2. **CAS** (*Contrast Adaptive Sharpening*) en dosis baja para devolver la definición que se pierde al agrandar.

Para anime hay un ajuste que prioriza las líneas, y para material fílmico uno que respeta el grano en lugar de "plastificarlo".

## Orientación automática

Los modos "Auto-Adaptativo" miran si el video es horizontal o vertical y eligen solos entre 1920×1080 y 1080×1920 (o sus versiones 2K y 4K). Así podés procesar en lote una carpeta mezclada sin configurar cada archivo.
