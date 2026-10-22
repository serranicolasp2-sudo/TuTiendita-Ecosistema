from django.http import HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.decorators.http import require_GET

from apps.contenido.cargador import contenido


def inicio(request):
    c = contenido()
    destacados = [p for p in c.proyectos if p.destacado]
    return render(
        request,
        "core/inicio.html",
        {"destacados": destacados, "guias": c.guias[:3], "total_proyectos": len(c.proyectos)},
    )


def sobre_mi(request):
    return render(request, "core/sobre_mi.html", {"proyectos": contenido().proyectos})


def foro(request):
    return render(request, "core/foro.html")


def campus(request):
    return render(request, "core/campus.html")


@require_GET
def robots(request):
    lineas = ["User-agent: *", "Allow: /", f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"]
    return render(request, "core/texto.txt", {"lineas": lineas}, content_type="text/plain; charset=utf-8")


@require_GET
def salud(request):
    """Lo usa deploy.sh para confirmar que la versión nueva responde. Si el contenido falla, falla esto."""
    c = contenido()
    return JsonResponse({"status": "ok", "proyectos": len(c.proyectos), "guias": len(c.guias)})


def favicon(request):
    """Los navegadores piden /favicon.ico aunque la página declare otro ícono.

    Se resuelve en cada pedido (no al cargar las URLs) porque en producción la ruta lleva el hash del manifiesto,
    que no existe hasta correr collectstatic, y `manage.py check` corre antes.
    """
    return HttpResponsePermanentRedirect(static("img/favicon.svg"))
