---
nombre: OmniBoost Studio
categoria: escritorio
estado: produccion
version: "1.0"
orden: 30
etiqueta: 7 presets · NVENC
resumen: Mejora la nitidez, limpia el ruido y saca las bandas de color de tus videos con filtros profesionales de FFmpeg.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, FFmpeg, CustomTkinter, PyInstaller]
repo: https://github.com/serranicolasp2-sudo/OmniBoost-Studio
incluido_en: omnisuite-studio
icono: img/proyectos/omniboost_256.png
datos:
  Filtros: CAS, hqdn3d, gradfun y unsharp
  Aceleración: NVIDIA NVENC, AMD AMF o CPU (libx264)
  Salida: MP4 H.264 / H.265 con audio AAC a 320 kbps
---

## Qué es

Una herramienta para "levantar" videos que llegan castigados: comprimidos por las redes, grabados con poca luz o generados con IA (Kling, Runway, Sora) con su típico parpadeo de grano y sus bandas en los degradados.

## Los filtros, sin vueltas

OmniBoost es una interfaz amigable sobre una cadena de filtros de FFmpeg bien calibrada:

| Problema | Filtro | Qué hace |
|---|---|---|
| Falta de nitidez | `cas` | *Contrast Adaptive Sharpening* de AMD: realza detalle sin halos blancos |
| Ruido y grano sucio | `hqdn3d` | Denoise espacial y temporal |
| Bandas en cielos y sombras | `gradfun` | Suaviza los escalones de color en degradados |
| Imagen chata | `unsharp` | Micro-contraste y sensación de profundidad |

Cada **preset** (Universal, Cine, 3D/CGI, Anime, Videos de IA, Restauración y Personalizado) es una combinación distinta de esas intensidades.

## Detalles que suman

- **Detecta la orientación**: los modos "Auto-Adaptativo" llevan un video horizontal a 1920×1080 y uno vertical a 1080×1920, sin recortar ni estirar.
- **Las resoluciones fijas no deforman**: si elegís 1080p, 2K o 4K y el video tiene otra proporción (por ejemplo, un vertical), lo encaja con barras negras en vez de estirarlo.
- **También mejora imágenes** (`.png`, `.jpg`, `.webp`) con los mismos filtros.
- **Procesamiento por lote**: le pasás una carpeta, con o sin subcarpetas, y sigue con el próximo archivo aunque uno esté dañado.
- **Nunca pisa el original**: guarda con el sufijo `_boosted.mp4`.
