from django.http import Http404
from django.shortcuts import render

from .cargador import CATEGORIAS, contenido


def proyectos(request):
    todos = contenido().proyectos
    grupos = [(nombre, [p for p in todos if p.categoria == clave]) for clave, nombre in CATEGORIAS.items()]
    return render(request, "contenido/proyectos.html", {"grupos": [g for g in grupos if g[1]]})


def proyecto(request, slug):
    c = contenido()
    p = c.proyecto(slug)
    if p is None:
        raise Http404("No existe ese proyecto")
    contexto = {"proyecto": p, "guias": c.guias_de(slug), "incluido_en": c.proyecto(p.incluido_en)}
    return render(request, "contenido/proyecto.html", contexto)


def guias(request):
    c = contenido()
    return render(
        request,
        "contenido/guias.html",
        {"guias": [(g, c.proyecto(g.proyecto)) for g in c.guias]},
    )


def guia(request, slug):
    c = contenido()
    g = c.guia(slug)
    if g is None:
        raise Http404("No existe esa guía")
    otras = [o for o in c.guias_de(g.proyecto) if o.slug != slug]
    return render(
        request, "contenido/guia.html", {"guia": g, "proyecto": c.proyecto(g.proyecto), "otras": otras}
    )
