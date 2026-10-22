# Auditoría: lo que dicen los README contra lo que hace el código

**Fecha:** 2026-10-22 · **Hecha por:** Claude Code, a pedido de Nicolás Serrano
**Para:** Antigravity (y cualquier agente que siga trabajando en estos repos)
**Alcance:** los 12 repos del ecosistema, en su rama por defecto (un commit cada uno, salvo `CFP-401-Avellaneda` con 31 y `Campus-Virtual-Semi` con 68).

## Cómo se verificó

- Se leyó cada `LEEME.md` / `README.md` y cada reporte (`REPORTE-MAESTRO-CONJUNTO.md`, `BITACORA-DE-INICIO.md`, `docs/TRASPASO.md`).
- Se contrastó cada afirmación técnica con el código fuente.
- Cuando se pudo, se **ejecutó el código real**: los métodos `_worker_thread` de OmniBoost, OmniFlow y OmniScale se corrieron sin interfaz (extraídos con `ast`) sobre un video de prueba generado con `ffmpeg -f lavfi -i testsrc`, con FFmpeg real en Linux y el codificador `libx264`. Se corrieron también los tests de `TuTiendita-Tienda`, `TuTiendita-Centralita` y `Campus-Virtual-Semi`.
- **Límites:** no hay Windows ni GPU en este entorno. Lo que depende de NVENC, AMF, PyInstaller o Inno Setup quedó marcado como **"verificar en Windows"**.

Cada hallazgo tiene **evidencia** (archivo:línea), **cómo reproducirlo** y una **propuesta**. Los números de línea corresponden al commit actual de cada repo.

---

## Resumen

| # | Repo | Hallazgo | Tipo | Estado |
|---|---|---|---|---|
| 1 | OmniBoost-Studio | El procesamiento se cae en el primer archivo y la interfaz queda colgada | 🔴 Error | Reproducido |
| 2 | OmniSuite-Studio | El botón "Lanzar" busca `.bat` que no existen en ningún repo | 🔴 Error | Verificar en Windows |
| 3 | TuTiendita-Centralita | No arranca con los repos separados (importa `tienda/` y `produccion/`) | 🔴 Error | Reproducido |
| 4 | Transcriptor-Local | La pestaña Configuración le muestra a todos el hardware de Nicolás | 🟠 Error menor | Confirmado en código |
| 5 | Transcriptor-Local | El README promete GPU CUDA; el código fuerza CPU | 🟠 README falso | Confirmado en código |
| 6 | Transcriptor-Local | El README describe un `.docx` con portada, tabla y colores que no existen | 🟠 README falso | Confirmado en código |
| 7 | OmniFlow-FPS-Booster | El README habla de "flujo óptico"; el código mezcla cuadros | 🟠 README falso | Confirmado y ejecutado |
| 8 | Omni Boost/Flow/Scale | Formatos de entrada y salida distintos a los documentados | 🟡 README impreciso | Confirmado y ejecutado |
| 9 | OmniBoost-Studio | "Realce HDR con preservación de tonos de piel" es un filtro `eq` | 🟡 README exagerado | Confirmado en código |
| 10 | OmniBoost-Studio | Las resoluciones fijas estiran los videos que no son 16:9 | 🟡 Comportamiento | Confirmado en código |
| 11 | OmniSuite-Studio | El instalador y el hub dependen de carpetas que no están en el repo | 🟡 Reproducibilidad | Confirmado en código |
| 12 | TuTiendita-Tienda | El README menciona SQLAlchemy y el SDK de Mercado Pago, que no se usan | 🟡 README impreciso | Confirmado en código |
| 13 | TuTiendita-Produccion / Centralita | Sin archivo de dependencias; Real-ESRGAN no viene en el repo | 🟡 Reproducibilidad | Confirmado |
| 14 | Campus-Virtual-Semi / Ecosistema | README y `CLAUDE.md` dicen 398 tests; hoy son 795, en verde, con 90 % de cobertura | 🟡 Documentación | Ejecutado |
| 15 | CFP-401-Avellaneda | La protección de claves y sesiones depende solo de `.htaccess` (Apache) | ℹ️ Advertencia | OK en el hosting actual |
| 16 | Todos | Frases de marketing no verificables ("plataforma líder", "referente") | ℹ️ Tono | — |

Lo que **sí coincide** está en la sección [Verificado y correcto](#verificado-y-correcto), al final.

---

## 🔴 1. OmniBoost: el procesamiento se cae en el primer archivo

**Evidencia.** `_probe_media` guarda el ancho y el alto como **texto**, porque salen tal cual de la salida de `ffprobe`:

```python
# app_video_booster.py:478-479
width = data.get("width", "?")
height = data.get("height", "?")
```

Después `_worker_thread` los compara con números, **fuera** del `try`:

```python
# app_video_booster.py:723
if in_w > 0 and in_h > 0:
```

(`_build_vf_filter`, en las líneas 512-513, hace lo mismo.)

**Qué ve el usuario.** El hilo de trabajo muere con `TypeError: '>' not supported between instances of 'str' and 'int'`. Nunca llega el mensaje `finished` a la cola, así que la interfaz queda en "procesando" para siempre. Pasa **siempre que `ffprobe` funciona**. Si `ffprobe` falla, `_probe_media` devuelve `None`, el ancho queda en `0` y el video se procesa, pero sin detectar la orientación.

**Reproducción.** Se ejecutó el `_worker_thread` real sobre un MP4 de 640×360:

```
EL HILO MUERE CON: TypeError '>' not supported between instances of 'str' and 'int'
¿Llegó el mensaje 'finished' a la interfaz?: False
```

**Propuesta (verificada).** Hacer lo mismo que ya hace OmniScale (`app_upscaler.py:530-531`):

```python
width = int(data.get("width", 0))
height = int(data.get("height", 0))
```

Con ese único cambio, el mismo test generó un 1080p correcto (`1920,1080,24/1`).

**Además:** revisar en `_on_res_change` / `_browse_*` (alrededor de la línea 386) si se usan `info["width"]` o `info["height"]` como número. Hoy se muestran como texto, así que no fallan.

---

## 🔴 2. OmniSuite: "Lanzar" apunta a archivos que no existen

**Evidencia.** El hub arma la ruta del lanzador con la carpeta padre de la app:

```python
# app_omnisuite_hub.py:459
bat_path = APPS_DIR / bat_name
```

Los nombres que busca (líneas 408, 416, 424 y 432) no están en ningún repo:

| Busca | Lo que hay en el repo de la app |
|---|---|
| `Lanzar OmniBoost.bat` | `OmniBoost-Studio/Lanzar Video Booster.bat` |
| `Lanzar OmniFlow.bat` | `OmniFlow-FPS-Booster/Lanzar FPS Booster.bat` y `Lanzar FPS Booster 60fps.bat` |
| `Lanzar OmniScale.bat` | `OmniScale-Studio/Lanzar Upscaler 1080p.bat` |
| `Lanzar Transcriptor.bat` | `Transcriptor-Local/transcribir.bat` |

**Instalado (verificar en Windows).** Con PyInstaller 6 en modo carpeta, `__file__` queda en `{app}\_internal\`, así que `APPS_DIR` pasa a ser `{app}`. El instalador de Inno Setup deja cada app en `{app}\<App>\<App>.exe`, sin ningún `.bat`. Si es así, "Lanzar" muestra "No se encontró el lanzador" en la versión instalada. La pestaña de instalación también busca `{app}\Instaladores\...` (línea 42), que no existe una vez instalado.

**Propuesta.**

- Si `getattr(sys, "frozen", False)`, lanzar directamente el `.exe` (`{app}\OmniBoost Studio\OmniBoost Studio.exe`, y así con cada app). En desarrollo, usar los `.bat` con sus nombres reales.
- En la versión instalada, ocultar o desactivar la pestaña "Instalar" (o hacer que descargue desde GitHub Releases).
- **Íconos (verificar):** el `.iss` usa `IconFilename: "{app}\iconos\*.ico"`, pero con PyInstaller 6 la carpeta `iconos` agregada con `--add-data` queda en `{app}\_internal\iconos`. Comprobar que los accesos directos muestren el ícono.

---

## 🔴 3. Centralita: no arranca con los repos separados

**Evidencia.** El servicio importa módulos de carpetas hermanas llamadas `tienda` y `produccion`, de cuando todo vivía en una sola carpeta:

```python
# servicio.py:25-29
TIENDA_DIR = AQUI.parents[0] / "tienda" / "herramientas"
sys.path.insert(0, str(AQUI.parents[0] / "tienda"))
sys.path.insert(0, str(AQUI.parents[0] / "produccion"))
```

Lo mismo pasa en `servicios/archivos.py:15-16`, `servicios/audio.py:16` y `servicios/audio.py:157`.

**Reproducción.** Con los repos clonados como están en GitHub:

```
$ pytest            # en TuTiendita-Centralita
E   ModuleNotFoundError: No module named 'carpetas'
```

Con enlaces `tienda -> TuTiendita-Tienda` y `produccion -> TuTiendita-Produccion` avanza, pero se corta en `ModuleNotFoundError: No module named 'msvcrt'`: los tests solo corren en Windows.

**Propuesta.**

- Leer las rutas desde variables de entorno (`TIENDA_DIR`, `PRODUCCION_DIR`) con el valor actual como default, y documentar en el `LEEME.md` la estructura de carpetas que espera.
- Agregar un `requirements.txt` (como mínimo `fastapi`, `uvicorn`, `httpx` y `Pillow`).
- Si se quiere CI en Linux, aislar lo que usa `msvcrt` detrás de un `if os.name == "nt"`.

---

## 🟠 4. Transcriptor: datos de hardware fijos en la pestaña Configuración

**Evidencia.**

```python
# src/gui.py:869-876
"• Backend: CPU (AMD Ryzen 7 5700X3D, 8 núcleos / 16 hilos)\n"
"• Memoria RAM: 32 GB (Consumo estimado: ~11 GB)\n"
"• Factor de Tiempo Real (RTF): ~0.96x (Validado con Prueba.mp3)\n"
```

Cualquier usuario ve el procesador y la RAM de la PC de desarrollo como si fueran los suyos.

**Propuesta.** Detectar el hardware real (`platform.processor()`, `psutil.cpu_count()`, `psutil.virtual_memory().total`), o rotular esos valores como "Referencia medida en el equipo de desarrollo".

**Dato útil para la documentación.** Esa referencia dice que la app usa **~11 GB de RAM** y tarda **~0,96× la duración del audio**. El `LEEME.md` de OmniSuite pide "8 GB mínimo": con 11 GB de consumo, ese mínimo no alcanza para el Transcriptor.

---

## 🟠 5. Transcriptor: el README promete GPU y el código usa solo CPU

**Afirmación.** `Transcriptor-Local/LEEME.md:89` dice que la pestaña Configuración "muestra si el pipeline se está ejecutando sobre GPU NVIDIA (CUDA con soporte FP16)". `OmniSuite-Studio/LEEME.md:77` habla de "GPU NVIDIA CUDA (FP16) o CPU". El README también recomienda una placa NVIDIA porque "acelera notablemente".

**Código.**

```python
# src/engine.py:54-58
WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", ...)
# src/engine.py:323
pipeline.to(torch.device("cpu"))
```

No hay ninguna rama que use CUDA.

**Propuesta.** Elegir una:

- **Corregir los README:** "funciona en CPU; no requiere placa de video".
- **Agregar GPU:** `device="cuda", compute_type="float16"` si `torch.cuda.is_available()`, con CPU como alternativa, y mostrar en Configuración el dispositivo que se usa de verdad. Ojo: el instalador tendría que incluir PyTorch con CUDA, y eso agranda mucho el paquete.

---

## 🟠 6. Transcriptor: el `.docx` no tiene lo que dice el README

**Afirmación** (`LEEME.md:113-114` y siguientes): portada con metadatos, "tabla estadística con la distribución del tiempo de habla por persona" y títulos en color por interlocutor.

**Código** (`src/exporter.py:51-110`): un título y un párrafo por intervención con `[hh:mm:ss] Hablante:` en negrita, siempre del mismo azul (`RGBColor(0, 51, 102)`). No hay portada, ni tabla, ni color por hablante.

**Propuesta.** Corregir el README o implementar lo que promete. La tabla es fácil de armar: sumar `end - start` por hablante a partir de los `segments`.

**Detalle relacionado.** El README dice "Pyannote Audio 3.1", pero el modelo principal es `pyannote/speaker-diarization-community-1` (`src/config.py:39`); 3.1 se usa solo si falla (`src/engine.py:316-321`).

---

## 🟠 7. OmniFlow: no usa flujo óptico

**Afirmación** (`LEEME.md:25` y `:41`): "algoritmos de flujo óptico bidireccional", "estimación de vectores por bloques cruzados", "anti-morphing".

**Código** (`app_fps_booster.py:428-436`):

| Método en la app | Filtro real |
|---|---|
| Universal adaptativo | `framerate=fps=N:interp_start=15:interp_end=240:scene=8.2` (mezcla de cuadros con detección de cortes) |
| Anime y 2D | `framerate=...:interp_start=5:interp_end=250:scene=5.0` |
| Motion Blend | `minterpolate=fps=N:mi_mode=blend` |
| Cadencia pura | `fps=N` (duplica cuadros) |

Ninguno usa compensación de movimiento (`minterpolate` con `mi_mode=mci`, que sí estima vectores de movimiento). **Los cuatro métodos funcionan:** se ejecutaron y los cuatro generaron 60 FPS.

**Propuesta.** Corregir el README para que describa la mezcla de cuadros con detección de cortes (que es honesto y útil), o sumar un modo "Interpolación por movimiento (lenta)" con `minterpolate=fps=N:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`. Ese modo sí estima movimiento bidireccional, pero es mucho más lento.

---

## 🟡 8. Formatos de entrada y salida distintos a los documentados (Boost, Flow y Scale)

| Afirmación del README | Código |
|---|---|
| Entrada: `.mp4 .mov .mkv .avi .webm .flv .ts .m4v .mpg .mpeg` | Se aceptan **solo** `.mp4 .mov .mkv .avi .webm` (`OmniFlow app_fps_booster.py:526`, `OmniBoost app_video_booster.py:640`, `OmniScale app_upscaler.py:483`). El selector de archivo único también filtra esas cinco. |
| Salida: "contenedor `.mp4` ... con audio AAC a 320 kbps" (OmniBoost `LEEME.md:95`) | Se **conserva la extensión de entrada** (`f"{p.stem}_{tag}{p.suffix}"`) y el audio se **copia tal cual** (`-c:a copy`, `app_video_booster.py:748`). |
| OmniFlow: guarda "en la misma carpeta" con sufijo `_60fps.mp4` | Crea la subcarpeta `Videos_60fps/` y conserva la extensión (`app_fps_booster.py:293-294`). |
| OmniBoost: sufijo `_boosted.mp4` | Sufijo `_1080p_boosted`, `_2k_boosted`, `_4k_boosted` o `_boosted`, dentro de `Videos_Boosted/`, `Videos_2K_Boosted/` o `Videos_4K_Boosted/`. |

**No documentado, pero bueno:** OmniBoost y OmniScale también procesan **imágenes** (`.png .jpg .jpeg .webp`), detectan formato **cuadrado (1:1)** y, si falla el codificador de GPU, **reintentan solos con CPU**. Conviene sumarlo a los README.

**Propuesta.** Ajustar los README al comportamiento real, o sumar las extensiones que faltan a `exts` y al filtro del diálogo. FFmpeg las lee sin problema.

---

## 🟡 9. OmniBoost: "Realce HDR con preservación de tonos de piel"

**Afirmación** (`LEEME.md:42`): "Expansión dinámica del color y contraste con preservación estricta de tonos de piel humana".

**Código** (`app_video_booster.py:545-549`): `eq=contrast=...:brightness=0.01:saturation=...:gamma=...`. Es un ajuste global, sin ninguna protección de tonos de piel ni procesamiento HDR.

**Propuesta.** Describirlo como "ajuste de contraste, saturación y gamma".

---

## 🟡 10. OmniBoost: las resoluciones fijas deforman

`scale=3840:2160`, `scale=1920:1080`, `scale=4096:2160` y `scale=2560:1440` (`app_video_booster.py:529-535`) **estiran** cualquier video que no tenga exactamente esa proporción, por ejemplo un vertical. Los modos "Auto-Adaptativo" sí la respetan.

**Propuesta.** Agregar `:force_original_aspect_ratio=decrease,pad=W:H:(ow-iw)/2:(oh-ih)/2`, como hace el modo Letterbox de OmniScale, o avisar en la interfaz.

---

## 🟡 11. OmniSuite: el build depende de carpetas fuera del repo

- `build_omnisuite.py` busca el Python en `../Transcriptor/entorno/Scripts/python.exe`.
- `OmniSuite_Installer.iss` empaqueta desde `{#Raiz}\Instaladores\0X ...\Portable\...`.
- El hub instala desde `APPS_DIR / "Instaladores"`.

Nada de eso existe al clonar el repo solo. Con lo que aclaró Nicolás (los binarios van a GitHub Releases y no a git), está bien que no estén versionados, pero **falta documentar la estructura de carpetas** que espera el build. Sin eso, nadie más puede compilar la suite.

**Propuesta.** Agregar al `LEEME.md` una sección "Cómo compilar" con el árbol de carpetas esperado, y publicar los `.exe` y `.zip` en **GitHub Releases** de cada repo. La web va a enlazar a `/releases/latest`. **Al 2026-10-22, ninguno de los 5 repos de escritorio tiene releases publicadas** (consultado con la API de GitHub), así que hoy esos enlaces muestran una página vacía.

---

## 🟡 12. Tienda: el README no describe bien la tecnología

| Afirmación | Código |
|---|---|
| "Base de datos: SQLite / SQLAlchemy" | `sqlite3` de la biblioteca estándar (`app/db.py`); SQLAlchemy no está en `requirements.txt` |
| "Integraciones: Mercado Pago SDK" | Llamadas HTTP directas con `httpx` a `api.mercadopago.com` (`app/mp.py:8`) |

**El README se queda corto en lo bueno:** valida la **firma de los webhooks** (`app/mp.py:71`, `firma_valida`), controla que el pago corresponda al pedido (`pago_corresponde`), concilia pagos pendientes y orquesta **Codex y Claude por CLI** sin usar la API paga (`herramientas/claudecli.py`, `herramientas/restauracion.py`). Los **46 tests pasan** ✅.

---

## 🟡 13. Producción y Centralita: sin archivo de dependencias

- `TuTiendita-Produccion` no tiene `requirements.txt`. Usa `Pillow`, `numpy` y `soundcard`.
- `herramientas/realesrgan/` solo tiene `README_windows.md` y dos imágenes de ejemplo. El `LEEME.md` dice que Real-ESRGAN viene "preconfigurado", pero `realesrgan-ncnn-vulkan.exe` y sus modelos hay que bajarlos aparte. Conviene dejar el link y la versión exacta (v0.2.5.0).
- `TuTiendita-Centralita` tampoco tiene `requirements.txt` (ver §3).

---

## 🟡 14. Campus: cifras de tests que no coinciden

| Documento | Cifra |
|---|---|
| `Campus-Virtual-Semi/README.md` ("estado al 2026-09-29") | 398 tests, 94 % de cobertura |
| `TuTiendita-Ecosistema/CLAUDE.md` | 398 tests unitarios |
| `Campus-Virtual-Semi/docs/TRASPASO.md` (entradas posteriores) | 753, 760, 761, 774 y 790 tests unitarios, más 21 E2E, según la entrada |

**Resultado real** (commit `3e6098d`, 2026-10-01, en este entorno): la suite junta **795 tests**, terminó **en verde** (código de salida 0) y la cobertura es **90,4 %** (8161 sentencias, 783 sin cubrir). Coincide con la entrada más reciente del traspaso (774 + 21 E2E). Los que quedaron atrasados son el README y `CLAUDE.md`. Las cifras intermedias del traspaso no siguen un orden creciente, así que no queda claro a qué commit corresponde cada una.

**Propuesta.** Actualizar el README y `CLAUDE.md` con la cifra real de la última corrida, y que cada entrada del traspaso diga fecha, hora y commit.

---

## ℹ️ 15. CFP: la protección de claves depende de Apache

El panel guarda los hashes en `site/api/.clave.json` y `.clave-maestra.json`, y las sesiones en `site/api/sesiones/`, **dentro de la carpeta pública**. Lo único que impide descargarlos son los `.htaccess` (`site/.htaccess`, `site/api/.htaccess`), y eso **solo funciona en Apache**.

- En el hosting actual (Ferozo / DonWeb, Apache), `BITACORA-DE-INICIO.md` y `REPORTE-MAESTRO-CONJUNTO.md` registran que se verificó en vivo un **403** sobre los dos `.clave*.json` y sobre `api/backups/`. ✅
- **No figura** la verificación de `api/sesiones/`. Conviene probarla: `curl -I https://cfp401avellaneda.com.ar/api/sesiones/` tiene que dar 403. (Desde este entorno no se pudo comprobar.)
- **Si algún día el sitio se muda al VPS con Nginx**, los `.htaccess` se ignoran. Hay que agregar reglas `location` equivalentes **antes** de subir los archivos, o mover `.clave*.json`, `sesiones/` y `backups/` fuera del webroot.

---

## ℹ️ 16. Tono de los README

Casi todos describen a Tu Tiendita IA como "plataforma y tienda **líder**" o "portal **referente**". El sitio todavía no está publicado: son frases que un lector técnico no puede comprobar y que le restan credibilidad al resto. Además, `CLAUDE.md` pide un tono "sin frases acartonadas". **Propuesta:** reemplazarlas por una línea concreta, por ejemplo: "Parte de las herramientas de Tu Tiendita IA (tutiendita-ia.store)".

---

## Verificado y correcto

| Repo | Qué se comprobó |
|---|---|
| OmniFlow-FPS-Booster | Los 4 métodos generan 60 FPS reales (ejecutado). CRF 16/18/20, NVENC p7 con AQ espacial y temporal, AMF, procesamiento recursivo de carpetas y alternativa automática a CPU: todo presente en el código. |
| OmniScale-Studio | El modo Auto-Adaptativo 1080p lleva un 640×360 a **1920×1080** (ejecutado). Lanczos + CAS, Spline36, Letterbox con `pad` y 1:1, como dice el README. |
| OmniBoost-Studio | Los 7 presets y los filtros `cas`, `hqdn3d`, `gradfun` y `unsharp` existen. Con el arreglo del §1, la salida es correcta (ejecutado). |
| Transcriptor-Local | faster-whisper `large-v3-turbo` int8 con VAD, pyannote, las 4 pestañas, el visor con reproducción por segmento, el monitoreo real de RAM con `psutil` y los modelos incluidos en el instalador (`instalador/Transcriptor.iss:48-49`). |
| Campus-Virtual-Semi | **795 tests en verde, 90,4 % de cobertura** (ejecutado). |
| TuTiendita-Tienda | 46 tests ✅. Webhooks con validación de firma, ntfy, CallMeBot, Drive, vigilante de precios con tope de 40 %. |
| TuTiendita-Centralita | Escucha solo en `127.0.0.1:8790`, exige el encabezado `X-Centralita: 1` y controla el `Host` contra DNS rebinding (`servicio.py:43-59`). |
| TuTiendita-Produccion | Real-ESRGAN `x4plus`, lado máximo de 4800 px a 300 DPI (`fotos.py:20,58,135`); 5 cambios por canción (`cancion.py:17`). |
| TuTiendita-Web | Están todas las páginas que lista el README (base, campaña Día de la Madre y gracias). |
| CFP-401-Avellaneda | bcrypt (`password_hash` / `password_verify`), límite de 5 intentos cada 15 minutos (`api/auth.php:61-92`), sesiones en carpeta propia. |
| Todos | **No se encontraron credenciales** en el código actual de ningún repo, ni en el historial de `CFP-401-Avellaneda`. Los tokens que aparecen son de ejemplo (`APP_USR-123`) en tests y documentación. |

---

## Orden sugerido

1. **§1 OmniBoost:** dos líneas, ya probadas. Recompilar y volver a publicar.
2. **§2 OmniSuite "Lanzar":** probar el instalado en Windows y corregir.
3. **§3 Centralita:** rutas configurables y `requirements.txt`.
4. **§5, §6 y §7:** decidir si se corrige el README o se implementa lo prometido. La web oficial va a describir **lo que hace el código hoy**.
5. Publicar los `.exe` y `.zip` en **GitHub Releases** de cada app (la web enlaza a `/releases/latest`).
6. Lo demás (§8 al §16) en una pasada de documentación.
