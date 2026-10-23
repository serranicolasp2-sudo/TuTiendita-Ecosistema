---
nombre: Tienda y bot de pedidos
categoria: servicios
estado: produccion
orden: 80
etiqueta: pago → bot → entrega
resumen: El backend que cobra con Mercado Pago, registra los pedidos y pone a trabajar al bot que los procesa.
stack: [Python, FastAPI, SQLAlchemy, SQLite, Mercado Pago, Google Drive API]
repo: https://github.com/serranicolasp2-sudo/TuTiendita-Tienda
icono: img/proyectos/tutiendita-tienda_256.png
datos:
  Pagos: Checkout Pro y webhooks con idempotencia
  Avisos: ntfy, WhatsApp y mail
  Respaldo: Google Drive
---

## Qué es

El núcleo comercial de los servicios. Recibe el pedido desde la web, cobra, avisa y deja todo listo para producir.

## Las piezas

- **API en FastAPI**: catálogo de productos, combos y cuadros; alta y seguimiento de pedidos; subida de fotos y datos para las canciones.
- **Mercado Pago**: cobro con Checkout Pro y confirmación por webhook. Los webhooks son **idempotentes**: si Mercado Pago avisa dos veces el mismo pago, el pedido no se duplica. Además, una tarea concilia los pagos que quedaron pendientes.
- **Bot de pedidos**: vigila los pedidos pagados, arma su carpeta de producción y arranca el proceso.
- **Vigilante de precios**: controla el costo de los insumos (cuadros, impresiones) para no vender por debajo del margen.
- **Avisos**: notificación inmediata al celular con ntfy, por WhatsApp y por mail.
- **Respaldo** de archivos y entregas en Google Drive.

## Cómo se conecta

Las landings de [Tu Canción](/proyectos/tu-cancion/) y [Restauración de Fotos](/proyectos/restauracion-de-fotos/) le mandan los pedidos; la [Centralita](/proyectos/tutiendita-centralita/) los muestra en la computadora de trabajo.
