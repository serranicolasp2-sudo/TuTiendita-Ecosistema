---
nombre: Campus Virtual Semipresencial
categoria: institucional
estado: desarrollo
orden: 100
destacado: true
etiqueta: 795 tests · 90 %
resumen: Un aula virtual hecha a medida en Django (no Moodle) para el secundario de adultos a distancia del CFP N° 401.
stack: [Python, Django 5.2, PostgreSQL, HTMX, django-allauth, Nginx, Gunicorn]
repo: https://github.com/serranicolasp2-sudo/Campus-Virtual-Semi
icono: img/proyectos/campus-virtual-semi_256.png
datos:
  Tests: 795 en verde, 90 % de cobertura
  Plan: 72 tareas en 10 etapas
  Personas: unas 240 en el padrón, 75 activas
---

## El problema

El secundario para adultos llevaba el seguimiento en una planilla Excel enorme: ocho hojas, cientos de formatos de celda distintos, DNI repetidos, mails en una misma celda. Los alumnos estudiaban con PDF sueltos y entregaban por mail. Moodle era demasiado para lo que se necesitaba y no leía esa planilla.

## La solución

Un campus propio donde:

- cada alumno ve **su trayecto**: qué materias tiene, cuáles aprobó y qué le falta;
- lee los PDF de cada unidad **dentro del campus**;
- **entrega** las actividades obligatorias y el docente las **corrige en la web**;
- hay foro y mensajería;
- se entra con mail o con Google, y el personal da de alta a los usuarios.

## Lo más difícil: la planilla

El importador lee la planilla real con vista previa antes de aplicar cambios y permite **revertir** una importación. Para construirlo se analizó el archivo celda por celda y se escribió una gramática que interpreta todos los formatos encontrados. Las pruebas usan una **copia sintética**, sin un solo dato real, que pasó dos chequeos independientes de fugas.

## Cómo se trabajó

El proyecto se planificó para construirse con agentes de IA (Claude, Codex y Gemini) trabajando en paralelo:

- un **contrato para agentes** con reglas, convenciones y definición de terminado;
- **72 tareas** con criterios de aceptación verificables, repartidas en etapas con dependencias explícitas;
- **revisión cruzada**: el código que escribe un agente lo revisa otro;
- **seguridad desde el diseño**: modelo de amenazas, archivos privados servidos solo a través de Nginx y checklist de privacidad por cambio.

Es el caso de estudio más completo de cómo encarar un sistema real con IA sin perder el control.
