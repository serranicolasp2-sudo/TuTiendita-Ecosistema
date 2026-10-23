---
nombre: Restauración de Fotos Antiguas
categoria: servicios
estado: produccion
orden: 70
destacado: true
etiqueta: real-esrgan x4 · 300 dpi
resumen: Recupera y colorea fotos familiares con IA y las lleva a calidad de impresión, con opción de cuadro.
stack: [Real-ESRGAN (ncnn-vulkan), Python, Pillow, FastAPI, Mercado Pago]
instagram: restauraciondefotos
web: https://restauraciondefotos.com.ar
repo: https://github.com/serranicolasp2-sudo/TuTiendita-Produccion
icono: img/proyectos/restauracion-de-fotos_256.png
datos:
  Modos de color: a color, colores de época o blanco y negro
  Salida: hasta 4800 px a 300 DPI
  Cuadros: ecocuero, madera o marco negro
---

## Qué es

Un servicio para recuperar fotos viejas: rayones, manchas, partes perdidas y color. El resultado se entrega en digital o impreso y enmarcado.

## El pipeline

La restauración en sí la hace un modelo de IA. Después, una herramienta propia (`fotos.py`) se encarga de todo lo repetitivo:

1. `nuevo RF-0001`: crea la carpeta del pedido con tres etapas: `1-original`, `2-codex` y `3-entrega`.
2. La foto restaurada se guarda en `2-codex` con el mismo nombre que la original.
3. `procesar RF-0001` genera tres archivos:
    - una **comparativa** antes/después, para controlar que las caras no cambien;
    - una **vista previa** chica y con marca de agua, para mandarle al cliente;
    - el **final**, escalado con **Real-ESRGAN x4** (ncnn-vulkan, por GPU) a 300 DPI y hasta 4800 px.
4. `listo RF-0001`: mueve el pedido a terminados.

Las fotos de los clientes nunca entran al repositorio: viven en una carpeta de trabajo aparte.

## La parte web

[restauraciondefotos.com.ar](https://restauraciondefotos.com.ar) tiene un comparador antes/después interactivo, un selector de modo de color y de cuadro, y está pensada primero para celular.
