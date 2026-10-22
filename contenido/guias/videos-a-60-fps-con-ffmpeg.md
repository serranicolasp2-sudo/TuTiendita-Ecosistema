---
titulo: Videos a 60 FPS con FFmpeg
resumen: Cómo llevar un video de 24 o 30 cuadros por segundo a 60 desde la terminal, con los mismos filtros que usa OmniFlow, y cuándo conviene cada uno.
proyecto: omniflow-fps-booster
nivel: inicial
duracion: 30 minutos
fecha: 2026-10-22
requisitos:
  - FFmpeg instalado
  - Un video corto para probar
  - Saber abrir una terminal
---

## Por qué un video "tironea"

Un video a 24 cuadros por segundo muestra 24 imágenes fijas por segundo. En una toma quieta no se nota; en un paneo rápido, el ojo ve los saltos entre una imagen y la siguiente. Pasa mucho con los videos generados por IA, que casi siempre salen a 24.

Para llevarlo a 60 hay que **inventar los cuadros que faltan** entre los originales. FFmpeg tiene tres formas de hacerlo, de la más simple a la más pesada.

## Paso 1: instalar FFmpeg y mirar tu video

En Windows:

```bash
winget install Gyan.FFmpeg
```

Cerrá y volvé a abrir la terminal. Después mirá a cuántos cuadros por segundo está tu video:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate,width,height -of default=noprint_wrappers=1 entrada.mp4
```

```text
width=1280
height=720
r_frame_rate=24/1
```

`24/1` quiere decir 24 cuadros por segundo.

## Paso 2: mezclar cuadros detectando los cortes (la opción por defecto)

```bash
ffmpeg -i entrada.mp4 -vf "framerate=fps=60:interp_start=15:interp_end=240:scene=8.2" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy salida_60fps.mp4
```

El filtro `framerate` arma cada cuadro nuevo **mezclando** los dos originales que tiene alrededor. Es rápido y no deforma nada.

- `interp_start` e `interp_end` marcan cuánto se mezcla. Con valores que van de 0 a 255, `15` y `240` dejan sin mezclar los cuadros que caen casi encima de un original: así se ven más nítidos.
- `scene=8.2` es la clave: **detecta los cortes de plano**. Sin esto, en cada corte aparecería un cuadro fantasma con la escena anterior y la nueva superpuestas.

Es el método **Universal Adaptativo** de OmniFlow.

### Para animación 2D

```bash
ffmpeg -i entrada.mp4 -vf "framerate=fps=60:interp_start=5:interp_end=250:scene=5.0" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy salida_anime.mp4
```

La animación tradicional repite dibujos ("anima a 2" o "a 3") y corta seco. Un `scene` más bajo detecta los cortes con más sensibilidad.

## Paso 3: suavizar paneos con `minterpolate` en modo mezcla

```bash
ffmpeg -i entrada.mp4 -vf "minterpolate=fps=60:mi_mode=blend" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy salida_blend.mp4
```

Es otra mezcla de cuadros, útil cuando el problema son los paneos rápidos. En OmniFlow es el método **Motion Blend**.

## Paso 4: interpolación por movimiento (la más pesada)

Los métodos anteriores **mezclan**: con un objeto que se mueve rápido, se ven dos copias semitransparentes. Para **calcular** dónde está cada parte de la imagen en el cuadro intermedio, `minterpolate` tiene un modo que estima vectores de movimiento:

```bash
ffmpeg -i entrada.mp4 -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy salida_mci.mp4
```

- `mi_mode=mci`: interpolación con compensación de movimiento.
- `me_mode=bidir`: busca el movimiento hacia adelante y hacia atrás.
- `mc_mode=aobmc` y `vsbmc=1`: suavizan los bordes de los bloques para que no se note la cuadrícula.

En OmniFlow es el método **Estimación de Movimiento Vectorial (MCI)**, con estos mismos parámetros.

!!! warning "Es lento y a veces deforma"
    En la prueba de esta guía, un clip de **3 segundos** en 720p tardó **40 segundos** en CPU: unas 13 veces su duración. Además, con movimientos complejos (manos, pelo, agua) puede dejar zonas "derretidas". Probalo en un fragmento corto antes de procesar un video entero.

## Paso 5: elegir el codificador

Todos los comandos de arriba usan la CPU (`libx264`). Las opciones que conviene conocer:

- `-crf 18` es la calidad: más bajo, mejor calidad y archivo más pesado. Entre 16 y 20 está bien para casi todo.
- `-c:a copy` copia el audio tal cual, sin recomprimirlo.
- `-pix_fmt yuv420p` asegura que el video se vea en cualquier reproductor y red social.

Si tenés una placa **NVIDIA RTX**, podés codificar con la placa, que es mucho más rápido. Estos son los parámetros que usa OmniFlow:

```bash
ffmpeg -i entrada.mp4 -vf "framerate=fps=60:scene=8.2" -c:v h264_nvenc -preset p7 -tune hq -multipass fullres -rc vbr -cq 18 -b:v 0 -spatial-aq 1 -temporal-aq 1 -pix_fmt yuv420p -c:a copy salida_nvenc.mp4
```

Ojo: la placa solo acelera la **codificación**. El cálculo de los cuadros nuevos (el filtro) sigue en la CPU.

## Paso 6: una carpeta entera de una vez

En Windows (PowerShell), parado en la carpeta de los videos:

```powershell
New-Item -ItemType Directory -Force "Videos_60fps" | Out-Null
Get-ChildItem *.mp4 | ForEach-Object {
  ffmpeg -hide_banner -i $_.FullName -vf "framerate=fps=60:scene=8.2" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy "Videos_60fps\$($_.BaseName)_60fps.mp4"
}
```

En macOS o Linux:

```bash
mkdir -p Videos_60fps
for f in *.mp4; do
  ffmpeg -hide_banner -i "$f" -vf "framerate=fps=60:scene=8.2" -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -c:a copy "Videos_60fps/${f%.mp4}_60fps.mp4"
done
```

Los resultados quedan en una subcarpeta aparte, así nunca se pisan los originales.

## Cuál usar

| Tu material | Método |
|---|---|
| Video real, 3D, videos de IA | `framerate` con `scene` (paso 2) |
| Animación 2D, anime | `framerate` con `scene` más bajo |
| Paneos que tironean | `minterpolate` en modo `blend` (paso 3) |
| Un plano clave donde la mezcla se nota | `minterpolate` en modo `mci` (paso 4), solo en ese fragmento |

## Para seguir

[OmniFlow FPS Booster](/proyectos/omniflow-fps-booster/) hace todo esto con una interfaz: elegís uno de los cinco métodos y el destino (48, 50, 60 o 120 FPS), procesa carpetas enteras y, si la placa de video falla, sigue solo con la CPU.
