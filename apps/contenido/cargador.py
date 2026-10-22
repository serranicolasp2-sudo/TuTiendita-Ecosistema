"""Lee los proyectos y las guías desde contenido/ (Markdown con encabezado YAML).

El contenido vive en el repo, no en la base: se escribe en Markdown, se versiona con git y se publica con un deploy.
Cada archivo empieza con un bloque YAML entre líneas `---` y sigue con el cuerpo en Markdown. Los campos están
documentados en contenido/LEEME.md.

Los archivos se vuelven a leer solo si cambió alguno (se compara la fecha de modificación), así que editar un .md
en el servidor se ve al instante sin reiniciar Gunicorn.
"""

from __future__ import annotations

import datetime as dt
import math
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

import markdown
import yaml
from django.conf import settings
from markdown.extensions.toc import slugify_unicode

CATEGORIAS = {
    "escritorio": "Software de escritorio",
    "servicios": "Servicios con IA",
    "institucional": "Desarrollo a medida",
}
ESTADOS = {
    "produccion": "En producción",
    "desarrollo": "En desarrollo",
    "piloto": "En piloto",
}
NIVELES = {
    "inicial": "Inicial",
    "intermedio": "Intermedio",
    "avanzado": "Avanzado",
}
PALABRAS_POR_MINUTO = 200
_SEPARADOR = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)


class ContenidoInvalido(Exception):
    """Un archivo de contenido/ tiene un error. El mensaje dice cuál y qué corregir."""


@dataclass(frozen=True)
class Descarga:
    nombre: str  # "Instalador", "Portable"…
    url: str
    tamano: str = ""  # como se muestra: "1,7 GB"


@dataclass(frozen=True)
class Proyecto:
    slug: str
    nombre: str
    categoria: str
    resumen: str
    estado: str
    etiqueta: str
    stack: tuple[str, ...]
    html: str
    toc: tuple[dict, ...]
    orden: int = 100
    destacado: bool = False
    version: str = ""
    plataforma: str = ""
    repo: str = ""
    web: str = ""
    instagram: str = ""  # usuario sin @
    icono: str = ""
    datos: tuple[tuple[str, str], ...] = ()
    descargas: tuple[Descarga, ...] = ()
    incluido_en: str = ""  # slug del proyecto con el que se descarga (las apps que vienen en OmniSuite)

    @property
    def categoria_nombre(self) -> str:
        return CATEGORIAS[self.categoria]

    @property
    def estado_nombre(self) -> str:
        return ESTADOS[self.estado]


@dataclass(frozen=True)
class Guia:
    slug: str
    titulo: str
    resumen: str
    proyecto: str
    nivel: str
    fecha: dt.date
    html: str
    toc: tuple[dict, ...]
    minutos_lectura: int
    duracion: str = ""
    actualizada: dt.date | None = None
    requisitos: tuple[str, ...] = ()
    borrador: bool = False

    @property
    def nivel_nombre(self) -> str:
        return NIVELES[self.nivel]


@dataclass(frozen=True)
class Contenido:
    proyectos: tuple[Proyecto, ...] = field(default_factory=tuple)
    guias: tuple[Guia, ...] = field(default_factory=tuple)

    def proyecto(self, slug: str) -> Proyecto | None:
        return next((p for p in self.proyectos if p.slug == slug), None)

    def guia(self, slug: str) -> Guia | None:
        return next((g for g in self.guias if g.slug == slug), None)

    def guias_de(self, proyecto_slug: str) -> list[Guia]:
        return [g for g in self.guias if g.proyecto == proyecto_slug]


def _markdown(cuerpo: str) -> tuple[str, tuple[dict, ...]]:
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "admonition", "toc", "codehilite"],
        extension_configs={
            "toc": {"slugify": slugify_unicode, "toc_depth": "2-3", "permalink": False},
            "codehilite": {"css_class": "codigo", "guess_lang": False},
        },
    )
    html = md.convert(cuerpo)
    return html, tuple(md.toc_tokens)


def _leer(ruta: Path) -> tuple[dict, str]:
    texto = ruta.read_text(encoding="utf-8")
    partes = _SEPARADOR.match(texto)
    if not partes:
        raise ContenidoInvalido(f"{ruta.name}: falta el encabezado YAML entre dos líneas '---' al principio")
    try:
        meta = yaml.safe_load(partes.group(1)) or {}
    except yaml.YAMLError as e:
        raise ContenidoInvalido(f"{ruta.name}: el encabezado YAML no se puede leer ({e})") from e
    return meta, partes.group(2)


def _exigir(meta: dict, ruta: Path, *campos: str) -> None:
    faltan = [c for c in campos if not meta.get(c)]
    if faltan:
        raise ContenidoInvalido(f"{ruta.name}: faltan los campos {', '.join(faltan)}")


def _elegir(meta: dict, ruta: Path, campo: str, opciones: dict) -> str:
    valor = meta.get(campo)
    if valor not in opciones:
        raise ContenidoInvalido(
            f"{ruta.name}: '{campo}' tiene que ser uno de {', '.join(opciones)} (dice {valor!r})"
        )
    return valor


def _descargas(meta: dict, ruta: Path) -> tuple[Descarga, ...]:
    """Un archivo de GitHub Releases ("archivo": nombre del asset, se baja de la última release) o una URL propia."""
    descargas = []
    for d in meta.get("descargas") or ():
        if not isinstance(d, dict) or not d.get("nombre") or not d.get("archivo"):
            raise ContenidoInvalido(f"{ruta.name}: cada descarga necesita 'nombre' y 'archivo'")
        archivo = str(d["archivo"])
        if archivo.startswith(("https://", "/")):
            url = archivo
        elif meta.get("repo"):
            url = f"{meta['repo']}/releases/latest/download/{archivo}"
        else:
            raise ContenidoInvalido(f"{ruta.name}: la descarga '{archivo}' necesita 'repo' (o una URL completa)")
        descargas.append(Descarga(str(d["nombre"]), url, str(d.get("tamano", ""))))
    return tuple(descargas)


def _proyecto(ruta: Path) -> Proyecto:
    meta, cuerpo = _leer(ruta)
    _exigir(meta, ruta, "nombre", "resumen", "etiqueta", "stack")
    html, toc = _markdown(cuerpo)
    return Proyecto(
        slug=ruta.stem,
        nombre=meta["nombre"],
        categoria=_elegir(meta, ruta, "categoria", CATEGORIAS),
        resumen=meta["resumen"],
        estado=_elegir(meta, ruta, "estado", ESTADOS),
        etiqueta=meta["etiqueta"],
        stack=tuple(meta["stack"]),
        html=html,
        toc=toc,
        orden=int(meta.get("orden", 100)),
        destacado=bool(meta.get("destacado", False)),
        version=str(meta.get("version", "")),
        plataforma=meta.get("plataforma", ""),
        repo=meta.get("repo", ""),
        web=meta.get("web", ""),
        instagram=str(meta.get("instagram", "")).lstrip("@"),
        icono=meta.get("icono", ""),
        datos=tuple((str(k), str(v)) for k, v in (meta.get("datos") or {}).items()),
        descargas=_descargas(meta, ruta),
        incluido_en=meta.get("incluido_en", ""),
    )


def _guia(ruta: Path, proyectos: set[str]) -> Guia:
    meta, cuerpo = _leer(ruta)
    _exigir(meta, ruta, "titulo", "resumen", "proyecto", "fecha")
    if meta["proyecto"] not in proyectos:
        raise ContenidoInvalido(
            f"{ruta.name}: el proyecto '{meta['proyecto']}' no existe en contenido/proyectos/"
        )
    for campo in ("fecha", "actualizada"):
        if meta.get(campo) is not None and not isinstance(meta[campo], dt.date):
            raise ContenidoInvalido(f"{ruta.name}: '{campo}' tiene que ser una fecha AAAA-MM-DD")
    html, toc = _markdown(cuerpo)
    return Guia(
        slug=ruta.stem,
        titulo=meta["titulo"],
        resumen=meta["resumen"],
        proyecto=meta["proyecto"],
        nivel=_elegir(meta, ruta, "nivel", NIVELES),
        fecha=meta["fecha"],
        html=html,
        toc=toc,
        minutos_lectura=max(1, math.ceil(len(cuerpo.split()) / PALABRAS_POR_MINUTO)),
        duracion=meta.get("duracion", ""),
        actualizada=meta.get("actualizada"),
        requisitos=tuple(meta.get("requisitos") or ()),
        borrador=bool(meta.get("borrador", False)),
    )


def leer_contenido(base: Path) -> Contenido:
    """Lee y valida todo contenido/. Lanza ContenidoInvalido ante el primer error."""
    proyectos = sorted(
        (_proyecto(r) for r in sorted((base / "proyectos").glob("*.md"))),
        key=lambda p: (p.orden, p.nombre),
    )
    slugs = {p.slug for p in proyectos}
    for p in proyectos:
        if p.incluido_en and p.incluido_en not in slugs:
            raise ContenidoInvalido(f"{p.slug}.md: 'incluido_en' apunta a '{p.incluido_en}', que no existe")
    guias = sorted(
        (_guia(r, slugs) for r in sorted((base / "guias").glob("*.md"))),
        key=lambda g: (g.fecha, g.slug),
        reverse=True,
    )
    return Contenido(proyectos=tuple(proyectos), guias=tuple(g for g in guias if not g.borrador))


_cache: dict = {"firma": None, "contenido": None}
_lock = threading.Lock()


def _firma(base: Path) -> tuple:
    return tuple((str(r), r.stat().st_mtime_ns) for r in sorted(base.glob("*/*.md")))


def contenido() -> Contenido:
    base = settings.CONTENIDO_DIR
    firma = _firma(base)
    with _lock:
        if _cache["firma"] != firma:
            _cache["contenido"] = leer_contenido(base)
            _cache["firma"] = firma
        return _cache["contenido"]
