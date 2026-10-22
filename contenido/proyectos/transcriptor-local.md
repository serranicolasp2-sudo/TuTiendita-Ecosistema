---
nombre: Transcriptor Local
categoria: escritorio
estado: produccion
version: "1.0"
orden: 20
destacado: true
etiqueta: whisper + pyannote
resumen: Transcribe audio y video sin internet y separa quién habla en cada momento. Exporta subtítulos, Word y texto.
plataforma: Windows 10 / 11 (64 bits)
stack: [Python, faster-whisper, pyannote.audio, PyTorch, CustomTkinter, python-docx]
repo: https://github.com/serranicolasp2-sudo/Transcriptor-Local
icono: img/proyectos/transcriptor_256.png
datos:
  Modelo de voz: Whisper large-v3-turbo (faster-whisper, int8)
  Hablantes: hasta 4, con pyannote
  Exporta: .srt, .docx, .txt y .json
---

## Qué es

Una app de escritorio que convierte cualquier audio o video en texto y además indica **quién dijo qué** (diarización). Funciona entera en tu computadora: no hay costo por minuto ni audios que viajen a un servidor ajeno.

Sirve para podcasts, entrevistas, clases, reuniones o declaraciones: cualquier grabación donde la privacidad importa o donde pagar por minuto se vuelve caro.

## Cómo funciona por dentro

El pipeline tiene cuatro pasos:

1. **Extracción de audio**: FFmpeg lo convierte a WAV mono de 16 kHz, el formato que esperan los modelos.
2. **Diarización**: `pyannote.audio` analiza la huella de cada voz y marca los tramos de cada hablante.
3. **Transcripción**: `faster-whisper` con el modelo `large-v3-turbo` en CPU, cuantizado a `int8`, con filtro de silencios (VAD) y marcas de tiempo por palabra.
4. **Ensamble**: cruza las dos líneas de tiempo y le asigna un hablante a cada frase.

El modelo de Whisper se carga una sola vez por proceso y queda protegido con un lock. Así la interfaz no se congela ni lo carga dos veces si apretás el botón de nuevo.

## Lo que entrega

- **.SRT** listo para Premiere, DaVinci, CapCut o YouTube.
- **.DOCX** con la transcripción agrupada por intervención: quién habla, desde qué minuto y qué dijo.
- **.TXT** limpio para copiar y pegar.
- **.JSON** con todos los tiempos y textos: es el archivo del proyecto, y lo podés reabrir en el visor.

## El visor y editor

Cada frase aparece en una tarjeta con su botón ▶: escuchás justo ese fragmento, corregís el texto o cambiás el hablante y volvés a exportar los cuatro archivos sin transcribir de nuevo.

## Paso a paso

Si querés armar uno propio, la guía [Tu propio transcriptor offline con Whisper y pyannote](/guias/transcriptor-offline-whisper-pyannote/) explica cómo, desde cero.
