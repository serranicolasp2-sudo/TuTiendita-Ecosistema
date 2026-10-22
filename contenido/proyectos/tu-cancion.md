---
nombre: Tu Canción
categoria: servicios
estado: produccion
orden: 60
destacado: true
etiqueta: letra + música a medida
resumen: Canciones personalizadas para regalar. La letra parte de la historia real de la persona y la música sale en el estilo que elijas.
stack: [LLM, Suno, Python, FFmpeg, FastAPI, Mercado Pago]
web: https://tucancion.com.ar
repo: https://github.com/serranicolasp2-sudo/TuTiendita-Produccion
datos:
  Estilos: balada, cumbia, rock y bolero, entre otros
  Vista previa: 1 minuto con fundido antes de aprobar
  Cambios: hasta 5 por pedido
---

## Qué es

Un servicio de canciones a medida: la persona cuenta la historia (cómo se conocieron, apodos, momentos), elige un estilo y recibe una canción única para regalar.

## Cómo se produce un pedido

Cada pedido sigue el mismo circuito, automatizado con una herramienta de línea de comandos (`cancion.py`):

1. `nuevo`: crea la carpeta del pedido con sus etapas (datos, letra, vistas previas, entrega) y un historial.
2. **Datos y letra**: con un cuestionario guiado se juntan los datos y un modelo de lenguaje propone la letra y el estilo, que reviso a mano.
3. **Música**: se generan variantes en Suno.
4. `previa`: graba automáticamente un minuto de muestra con fundido para mandarle al cliente.
5. `cambio`: registra cada ajuste pedido (hasta cinco).
6. `final` y `listo`: arma el entregable con el nombre del destinatario y archiva el pedido.

## La parte web

La landing de [tucancion.com.ar](https://tucancion.com.ar) tiene reproductor con muestras reales, un formulario de pedido guiado y cobro con Mercado Pago, conectado al [backend de la tienda](/proyectos/tutiendita-tienda/).
