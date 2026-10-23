---
nombre: Portal del CFP N° 401 Avellaneda
categoria: institucional
estado: produccion
orden: 110
destacado: true
etiqueta: web + CMS + flyers
resumen: El sitio oficial de la escuela, un panel para que el equipo actualice los cursos sin tocar código y un generador de flyers para redes.
stack: [React, JSX, PHP, bcrypt, Nginx]
web: https://cfp401avellaneda.com.ar
repo: https://github.com/serranicolasp2-sudo/CFP-401-Avellaneda
icono: img/proyectos/cfp401-portal_256.png
datos:
  Flyers: feed 1:1 y 4:5, historias 9:16 y afiches A4
  Panel: login con bcrypt, CSRF y límite de intentos
---

## Qué es

El portal institucional de un Centro de Formación Profesional de la Provincia de Buenos Aires. Tiene tres partes:

1. **Sitio público**: catálogo de cursos gratuitos con buscador en vivo, filtros por familia profesional y turno, y fichas que se comparten bien por WhatsApp (con vista previa propia de cada curso).
2. **Panel de administración**: el equipo carga cursos, vacantes, estados de inscripción y novedades sin tocar código.
3. **Generador de flyers**: a partir de los datos de un curso arma la pieza para redes o para imprimir, con la identidad de la escuela.

## Seguridad en un hosting simple

El panel corre sobre PHP en un servidor común, sin base de datos. Para que eso sea seguro:

- contraseñas con **bcrypt** y dos niveles de clave (equipo y maestra);
- sesiones `HttpOnly`, protección **CSRF** y **límite de intentos**;
- **escritura atómica** del archivo de datos con copias de respaldo rotativas, para que un guardado cortado no rompa el sitio.

## Sistema de diseño

Incluye los tokens de diseño de la institución, guías de marca, componentes y una fototeca de los talleres, para que cualquier pieza nueva salga coherente.
