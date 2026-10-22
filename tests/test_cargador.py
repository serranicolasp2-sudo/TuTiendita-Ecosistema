import datetime as dt
import os
from textwrap import dedent

import pytest
from django.conf import settings

from apps.contenido.cargador import ContenidoInvalido, contenido, leer_contenido

PROYECTO = """\
---
nombre: Demo
categoria: escritorio
estado: produccion
etiqueta: nota
resumen: Un proyecto de prueba.
stack: [Python]
repo: https://github.com/ejemplo/Demo
---
## Qué es

Texto con `código`.
"""

GUIA = """\
---
titulo: Guía demo
resumen: Una guía.
proyecto: demo
nivel: inicial
fecha: 2026-10-01
---
## Paso 1

Hacé esto.
"""


def _escribir(base, proyectos=None, guias=None):
    (base / "proyectos").mkdir()
    (base / "guias").mkdir()
    for nombre, texto in (proyectos or {}).items():
        (base / "proyectos" / f"{nombre}.md").write_text(dedent(texto), encoding="utf-8")
    for nombre, texto in (guias or {}).items():
        (base / "guias" / f"{nombre}.md").write_text(dedent(texto), encoding="utf-8")
    return base


def test_el_contenido_real_del_repo_es_valido():
    c = leer_contenido(settings.CONTENIDO_DIR)
    assert c.proyectos and c.guias
    slugs = {p.slug for p in c.proyectos}
    assert all(g.proyecto in slugs for g in c.guias)


def test_lee_proyecto_y_guia(tmp_path):
    c = leer_contenido(_escribir(tmp_path, {"demo": PROYECTO}, {"guia-demo": GUIA}))
    p = c.proyecto("demo")
    assert p.nombre == "Demo" and p.categoria_nombre == "Software de escritorio"
    assert "<code>código</code>" in p.html
    assert p.toc[0]["id"] == "qué-es"
    assert p.descarga == "https://github.com/ejemplo/Demo/releases/latest"
    g = c.guia("guia-demo")
    assert g.fecha == dt.date(2026, 10, 1) and g.minutos_lectura == 1
    assert c.guias_de("demo") == [g]


def test_solo_el_software_de_escritorio_tiene_descarga(tmp_path):
    servicio = PROYECTO.replace("categoria: escritorio", "categoria: servicios")
    assert leer_contenido(_escribir(tmp_path, {"demo": servicio})).proyecto("demo").descarga == ""


def test_los_borradores_no_se_publican(tmp_path):
    borrador = GUIA.replace("nivel: inicial", "nivel: inicial\nborrador: true")
    assert leer_contenido(_escribir(tmp_path, {"demo": PROYECTO}, {"g": borrador})).guias == ()


@pytest.mark.parametrize(
    ("proyectos", "guias", "mensaje"),
    [
        ({"demo": "sin encabezado"}, {}, "falta el encabezado YAML"),
        ({"demo": PROYECTO.replace("nombre: Demo\n", "")}, {}, "faltan los campos nombre"),
        ({"demo": PROYECTO.replace("escritorio", "juegos")}, {}, "'categoria' tiene que ser uno de"),
        (
            {"demo": PROYECTO},
            {"g": GUIA.replace("proyecto: demo", "proyecto: otro")},
            "el proyecto 'otro' no existe",
        ),
        ({"demo": PROYECTO}, {"g": GUIA.replace("2026-10-01", "ayer")}, "'fecha' tiene que ser una fecha"),
    ],
)
def test_errores_de_contenido_dicen_que_corregir(tmp_path, proyectos, guias, mensaje):
    with pytest.raises(ContenidoInvalido, match=mensaje):
        leer_contenido(_escribir(tmp_path, proyectos, guias))


def test_un_md_editado_se_ve_sin_reiniciar(tmp_path, settings):
    settings.CONTENIDO_DIR = _escribir(tmp_path, {"demo": PROYECTO})
    assert contenido().proyecto("demo").nombre == "Demo"
    ruta = tmp_path / "proyectos" / "demo.md"
    ruta.write_text(PROYECTO.replace("nombre: Demo", "nombre: Demo 2"), encoding="utf-8")
    os.utime(
        ruta, ns=(1, 2_000_000_000_000_000_000)
    )  # fecha de modificación distinta aunque pase el mismo instante
    assert contenido().proyecto("demo").nombre == "Demo 2"
