---
titulo: Tu propio transcriptor offline con Whisper y pyannote
resumen: Un script de Python que transcribe audio o video sin internet, separa quién habla y genera subtítulos .srt. La misma base del Transcriptor Local, explicada paso a paso.
proyecto: transcriptor-local
nivel: intermedio
duracion: 1 hora
fecha: 2026-10-22
requisitos:
  - Windows, macOS o Linux con 16 GB de RAM
  - Python 3.10 o más nuevo
  - FFmpeg instalado
  - Una cuenta gratuita en Hugging Face
---

## Qué vas a armar

Un script que recibe una grabación (una entrevista, una clase, un podcast) y devuelve un archivo de subtítulos así:

```text
1
00:00:00,000 --> 00:00:03,800
[Hablante 1]: Hola, bienvenidos al programa.

2
00:00:03,800 --> 00:00:08,560
[Hablante 2]: Gracias por invitarme.
```

Todo corre en tu computadora: después de la primera descarga de los modelos, no necesita internet y no se paga por minuto.

Usa dos modelos que hacen cosas distintas:

- **Whisper** (con `faster-whisper`) escucha y escribe **qué** se dijo, con el minuto exacto de cada frase.
- **pyannote** no entiende palabras: reconoce **voces**. Devuelve tramos de tiempo del tipo "de 0 a 3,8 s habló la voz A".

El truco está en cruzar las dos líneas de tiempo.

## Paso 1: preparar el entorno

Creá una carpeta para el proyecto y un entorno virtual adentro:

```bash
mkdir transcriptor && cd transcriptor
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

Instalá primero PyTorch **en su versión para CPU**. Si no, pip baja la versión con CUDA, que pesa varios GB:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install faster-whisper pyannote.audio soundfile
```

Comprobá que FFmpeg responde:

```bash
ffmpeg -version
```

Si no lo tenés, en Windows se instala con `winget install Gyan.FFmpeg` (cerrá y volvé a abrir la terminal después).

## Paso 2: permiso para el modelo de voces

El modelo de pyannote es gratuito, pero pide aceptar sus condiciones de uso:

1. Entrá a [huggingface.co/pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) con tu cuenta y aceptá las condiciones.
2. En **Settings → Access Tokens**, creá un token de tipo **Read**.
3. Cargalo como variable de entorno en la terminal donde vas a correr el script:

```bash
# Windows (PowerShell):
$env:HF_TOKEN = "hf_tu_token"
# macOS / Linux:
export HF_TOKEN="hf_tu_token"
```

El token se usa **solo la primera vez**, para descargar el modelo. El script guarda los modelos en la carpeta `modelos/` y desde ahí funciona sin conexión.

!!! warning "No subas el token a ningún lado"
    No lo escribas dentro del código ni lo subas a GitHub. Si se filtra, borralo en Hugging Face y creá otro.

## Paso 3: llevar el audio al formato de los modelos

Los dos modelos trabajan con audio **mono a 16 kHz**. FFmpeg convierte cualquier cosa (mp3, m4a, mp4, mkv…) a ese formato:

```python
def a_wav(entrada: Path) -> Path:
    wav = entrada.with_name(entrada.stem + "_16k.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(entrada), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)],
        check=True,
    )
    return wav
```

Después el script lo lee **una sola vez** con `soundfile` y le pasa ese mismo audio a los dos modelos.

!!! note "Por qué no le pasamos el archivo directo a Whisper"
    `faster-whisper` puede abrir el archivo solo, pero para eso usa la librería PyAV, y algunas combinaciones de versiones fallan (`faster-whisper` 1.2.1 con `av` 19 da `unexpected keyword argument 'metadata_errors'`). Como FFmpeg ya hizo la conversión, le pasamos el audio cargado y evitamos el problema.

## Paso 4: transcribir con Whisper

```python
whisper = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", download_root=str(MODELOS))
segmentos, _info = whisper.transcribe(
    audio,
    language="es",
    beam_size=5,
    vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 500, "speech_pad_ms": 400},
)
```

Las tres decisiones que importan:

- **`large-v3-turbo`** es la mejor relación calidad/velocidad de la familia Whisper. Si tu PC tiene poca RAM, probá con `small` (se elige con la variable `MODELO_WHISPER`).
- **`compute_type="int8"`** cuantiza el modelo: usa bastante menos memoria y en CPU va más rápido, con una pérdida de precisión que casi no se nota.
- **`vad_filter=True`** saltea los silencios antes de transcribir. Ahorra tiempo y evita que Whisper "invente" frases en los tramos sin voz, un error clásico.

## Paso 5: separar las voces con pyannote

```python
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=token)
entrada = {"waveform": torch.from_numpy(audio).unsqueeze(0), "sample_rate": 16000}
salida = pipeline(entrada, num_speakers=2)
```

- Si sabés cuántas personas hablan, pasalo con `num_speakers`: el resultado mejora mucho. Si no, sacalo y pyannote lo estima solo.
- Le pasamos el audio ya cargado en memoria en vez de la ruta: así no depende de otras librerías para leer el archivo.
- La versión 4 de pyannote devuelve el resultado en `salida.speaker_diarization`; la 3 lo devuelve directo. El script contempla las dos.

## Paso 6: cruzar las dos líneas de tiempo

Ahora tenemos frases con tiempos (Whisper) y tramos de voz con tiempos (pyannote). A cada frase le asignamos la voz con la que **más se superpone**:

```python
def solape(a: dict, b: dict) -> float:
    return max(0.0, min(a["fin"], b["fin"]) - max(a["inicio"], b["inicio"]))
```

Si una frase cae justo en un hueco y no se pisa con ningún tramo, le toca el tramo más cercano. Las etiquetas internas (`SPEAKER_00`, `SPEAKER_01`) se renombran por orden de aparición: **Hablante 1** es el primero que habla.

## Paso 7: el script completo

Guardalo como `transcribir.py`:

```python
"""Transcriptor offline con Whisper + pyannote.

Uso:  python transcribir.py entrevista.mp3 [cantidad_de_hablantes]
Genera entrevista.srt al lado del archivo original.
"""

import os
import subprocess
import sys
from pathlib import Path

MODELOS = Path(__file__).resolve().parent / "modelos"
# Antes de importar las librerías: los modelos se guardan en ./modelos y no en la carpeta del usuario.
os.environ.setdefault("HF_HUB_CACHE", str(MODELOS))

import soundfile as sf  # noqa: E402
import torch  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402
from pyannote.audio import Pipeline  # noqa: E402

MODELO_WHISPER = os.environ.get("MODELO_WHISPER", "large-v3-turbo")


def a_wav(entrada: Path) -> Path:
    """Convierte cualquier audio o video a WAV mono de 16 kHz, el formato que esperan los modelos."""
    wav = entrada.with_name(entrada.stem + "_16k.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(entrada), "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(wav)],
        check=True,
    )
    return wav


def transcribir(audio) -> list[dict]:
    whisper = WhisperModel(MODELO_WHISPER, device="cpu", compute_type="int8", download_root=str(MODELOS))
    segmentos, _info = whisper.transcribe(
        audio,  # el audio ya cargado: así faster-whisper no necesita decodificar el archivo
        language="es",
        beam_size=5,
        vad_filter=True,  # saltea los silencios: más rápido y sin frases inventadas
        vad_parameters={"min_silence_duration_ms": 500, "speech_pad_ms": 400},
    )
    return [{"inicio": s.start, "fin": s.end, "texto": s.text.strip()} for s in segmentos]


def diarizar(audio, token: str | None, hablantes: int | None = None) -> list[dict]:
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=token)
    entrada = {"waveform": torch.from_numpy(audio).unsqueeze(0), "sample_rate": 16000}
    salida = pipeline(entrada, **({"num_speakers": hablantes} if hablantes else {}))
    # pyannote 4 devuelve un objeto con .speaker_diarization; pyannote 3 devuelve la anotación directamente.
    anotacion = getattr(salida, "speaker_diarization", salida)
    return [{"inicio": t.start, "fin": t.end, "hablante": h} for t, _, h in anotacion.itertracks(yield_label=True)]


def solape(a: dict, b: dict) -> float:
    """Cuántos segundos se pisan dos tramos de tiempo."""
    return max(0.0, min(a["fin"], b["fin"]) - max(a["inicio"], b["inicio"]))


def centro(a: dict) -> float:
    return (a["inicio"] + a["fin"]) / 2


def asignar_hablantes(frases: list[dict], turnos: list[dict]) -> list[dict]:
    """A cada frase le toca el hablante con el que más se superpone en el tiempo."""
    nombres = {}
    for t in sorted(turnos, key=lambda t: t["inicio"]):  # Hablante 1 = el primero que habla
        nombres.setdefault(t["hablante"], f"Hablante {len(nombres) + 1}")

    for f in frases:
        mejor = max(turnos, key=lambda t: solape(f, t), default=None)
        if mejor is not None and solape(f, mejor) == 0:  # no se pisa con ningún turno: el más cercano
            mejor = min(turnos, key=lambda t: abs(centro(t) - centro(f)))
        f["hablante"] = nombres[mejor["hablante"]] if mejor else "Hablante ?"
    return frases


def tiempo_srt(segundos: float) -> str:
    ms = round(segundos * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def guardar_srt(frases: list[dict], ruta: Path) -> None:
    bloques = [
        f"{i}\n{tiempo_srt(f['inicio'])} --> {tiempo_srt(f['fin'])}\n[{f['hablante']}]: {f['texto']}\n"
        for i, f in enumerate(frases, 1)
    ]
    ruta.write_text("\n".join(bloques), encoding="utf-8")


if __name__ == "__main__":
    entrada = Path(sys.argv[1])
    hablantes = int(sys.argv[2]) if len(sys.argv) > 2 else None
    audio, _ = sf.read(str(a_wav(entrada)), dtype="float32")
    print("Transcribiendo…")
    frases = transcribir(audio)
    print("Separando hablantes…")
    turnos = diarizar(audio, os.environ.get("HF_TOKEN"), hablantes)
    frases = asignar_hablantes(frases, turnos)
    guardar_srt(frases, entrada.with_suffix(".srt"))
    for f in frases:
        print(f"[{tiempo_srt(f['inicio'])}] {f['hablante']}: {f['texto']}")
    print(f"Listo: {entrada.with_suffix('.srt')}")
```

Y corrélo:

```bash
python transcribir.py entrevista.mp3 2
```

El `2` es la cantidad de hablantes; es opcional. El `.srt` queda al lado del audio y se importa directo en Premiere, DaVinci Resolve, CapCut o YouTube.

## Cuánto tarda y cuánta memoria usa

Una referencia real del Transcriptor Local, que usa estos mismos modelos: en un **Ryzen 7 5700X3D** con 32 GB, todo el proceso tarda **más o menos lo mismo que dura el audio** (una hora de entrevista, una hora de proceso) y usa unos **11 GB de RAM**.

Con 8 GB, usá `MODELO_WHISPER=small` y cerrá otros programas.

## Para seguir

Este script es el corazón del [Transcriptor Local](/proyectos/transcriptor-local/). Lo que la app suma encima:

- una interfaz para elegir el archivo y ver el progreso;
- un visor para escuchar cada frase y corregirla;
- la exportación a `.docx`, `.txt` y `.json`;
- un instalador que trae los modelos adentro, para no necesitar token ni internet.

Buenos ejercicios para practicar: exportar también un `.txt` agrupando las frases seguidas del mismo hablante, o permitir ponerles nombre a los hablantes ("Entrevistador", "Invitada").
