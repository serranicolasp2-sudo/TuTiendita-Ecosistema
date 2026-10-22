---
nombre: OmniSuite Studio
categoria: escritorio
estado: produccion
version: "1.0"
orden: 10
destacado: true
etiqueta: 4 apps · 1 instalador
resumen: El hub que junta todas mis herramientas de video y audio en un solo instalador para Windows, 100 % offline.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, CustomTkinter, FFmpeg, PyInstaller, Inno Setup]
repo: https://github.com/serranicolasp2-sudo/OmniSuite-Studio
icono: img/proyectos/omnisuite_256.png
datos:
  Incluye: OmniBoost, OmniFlow, OmniScale y Transcriptor Local
  Formatos: Instalador .exe y versión portable .zip
  Requisitos: 8 GB de RAM (16 recomendados), 6 GB de disco
---

## Qué es

OmniSuite Studio es el centro de control de la suite. Desde una sola ventana elegís qué herramientas instalar, las abrís con un clic o armás una versión portable para llevar en un pendrive.

Nació de un problema concreto: cada app tenía su propio instalador, sus propias dependencias y su propia copia de FFmpeg. Instalar las cuatro era repetir cuatro veces lo mismo.

## Qué resuelve

Cubre los cuatro cuellos de botella más comunes al producir video para redes:

- **Nitidez y limpieza** del material comprimido o generado con IA → [OmniBoost Studio](/proyectos/omniboost-studio/)
- **Fluidez**: pasar de 24/30 a 60 FPS → [OmniFlow FPS Booster](/proyectos/omniflow-fps-booster/)
- **Resolución y formato**: llevar a 1080p o 4K, horizontal o vertical → [OmniScale Studio](/proyectos/omniscale-studio/)
- **Subtítulos y transcripción** con quién habla en cada momento → [Transcriptor Local](/proyectos/transcriptor-local/)

## Cómo está armado

- **Hub** (`app_omnisuite_hub.py`): interfaz en CustomTkinter con el tema visual de la marca, compartido entre todas las apps (`ui_theme.py`).
- **Empaquetado**: cada app se compila con PyInstaller en un `.exe` sin ventana de consola, con FFmpeg dentro de la carpeta `_internal`.
- **Instalador**: un script de Inno Setup (`OmniSuite_Installer.iss`) con casillas para elegir qué apps instalar. Crea el grupo en el menú Inicio y los accesos directos.
- **Portable**: `ensamblar_suite_portable.py` arma un `.zip` que funciona sin permisos de administrador.

## Por qué offline

Todo el procesamiento pasa en tu computadora: no se sube ningún video, no hay suscripción y no se paga por minuto. Para un creador que trabaja con material de clientes, eso es privacidad y costo fijo.
