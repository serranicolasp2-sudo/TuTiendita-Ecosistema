---
nombre: OmniVideo Studio
categoria: escritorio
estado: produccion
version: "1.0"
orden: 15
destacado: true
etiqueta: 3 en 1 · Modo Cadena · 123 MB
resumen: Suite unificada de video. Mejora con IA, interpolación a 60 FPS y escalado a 4K en una sola pasada de FFmpeg sin pérdida de calidad.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, omni_core, FFmpeg, PyInstaller, Inno Setup]
repo: https://github.com/serranicolasp2-sudo/OmniVideo-Studio
descargas:
  - nombre: Instalador
    archivo: OmniVideo.Studio.Instalador.1.0.exe
    tamano: 123 MB
  - nombre: Portable
    archivo: OmniVideo.Studio.Portable.zip
    tamano: 176 MB
icono: img/proyectos/omnivideo_256.png
datos:
  Modos: Mejorar (CAS/Denoise), Fluidez (HFR 60/120 FPS), Escalar (1080p/2K/4K) y Cadena
  Aceleración: NVIDIA NVENC (P7 HQ multipass), AMD AMF, CPU (libx264)
  Optimización: Núcleo compartido omni_core, 1 sola copia de FFmpeg, 0 recompresiones intermedias
---

## Qué es

OmniVideo Studio es la evolución natural del flujo de video en Tu Tiendita IA: unifica en una sola aplicación de escritorio los tres motores de procesamiento (**OmniBoost**, **OmniFlow** y **OmniScale**), compartiendo un mismo núcleo (`omni_core`) y un solo binario de FFmpeg.

## El problema que resuelve

Anteriormente, para mejorar un video, darle fluidez a 60 FPS y escalarlo a 4K, el creador debía exportar tres veces seguidas en tres programas distintos. Cada pasada implicaba esperar el triple de tiempo y recomprimir el video, sufriendo pérdida de nitidez generacional.

Con **OmniVideo Studio**:
- **Modo Cadena (Single-Pass Pipeline)**: Unifica la limpieza de ruido, el contraste adaptativo CAS, la interpolación de cuadros y el escalado Lanczos/Spline36 en una única pasada de FFmpeg.
- **Sin pérdida generacional**: Se codifica directamente de origen a destino final una sola vez.
- **Peso reducido**: De los 588 MB de los tres portables anteriores a solo **123 MB** en el instalador y **176 MB** en la versión portable.

## Modos integrados

1. **🎬 Mejorar (OmniBoost)**: Contraste adaptativo CAS, reducción de grano `hqdn3d`, eliminación de bandas `gradfun` y realce de micro-contraste.
2. **⚡ Fluidez (OmniFlow)**: Interpolación a 48, 50, 60 o 120 FPS mediante flujo óptico bidireccional (`minterpolate` MCI) o cadencia suave.
3. **📱 Escalar (OmniScale)**: Upscaling a 1080p, 2K o 4K adaptativo (horizontal 16:9, vertical 9:16 para Reels/TikTok o 1:1 cuadrado) con algoritmos Lanczos y Spline36.
4. **🔗 Cadena (Pipeline Unificado)**: Los tres procesos encadenados en un único grafo de filtros en memoria.

## Cómo se descarga

Está disponible tanto como **instalador para Windows** con integración al Menú Inicio y accesos directos, como en **versión portable autónoma en .zip** para llevar en un pendrive y usar sin conexión a internet ni dependencias externas.
