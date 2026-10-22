---
nombre: Centralita de pedidos
categoria: servicios
estado: produccion
orden: 90
etiqueta: panel local
resumen: Un panel que corre en la computadora de trabajo y muestra en tiempo real qué pedidos entran, cuáles están en proceso y cuáles están listos.
stack: [Python, FastAPI, HTML, JavaScript]
repo: https://github.com/serranicolasp2-sudo/TuTiendita-Centralita
datos:
  Corre en: la propia PC, sin exponerse a internet
  Módulos: archivos, audio, clientes, costos, retoques y sistema
---

## Qué es

La tienda vive en un servidor, pero la producción (restaurar, componer, imprimir) pasa en una computadora. La Centralita es el puente: un servicio local con su panel en el navegador.

## Qué hace

- Muestra los pedidos entrantes, en proceso y listos, y el estado de los bots.
- Abre las carpetas de cada pedido, compara fotos antes/después y reproduce los audios.
- Calcula costos de impresión y cuadros para cotizar.
- Registra los retoques que pide cada cliente.

## Seguridad de un servicio local

Que algo corra en tu propia PC no lo vuelve seguro solo. El servicio escucha únicamente en la propia máquina, exige un encabezado propio en cada pedido (así otra página abierta en el navegador no le puede hablar) y valida cada ruta de archivo para que nadie pueda salir de la carpeta de pedidos.
