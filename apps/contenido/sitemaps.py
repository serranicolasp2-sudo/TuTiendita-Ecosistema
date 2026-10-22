from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .cargador import contenido


class PaginasSitemap(Sitemap):
    def items(self):
        return ["inicio", "proyectos", "guias", "sobre_mi", "foro", "campus"]

    def location(self, item):
        return reverse(item)


class ProyectosSitemap(Sitemap):
    def items(self):
        return list(contenido().proyectos)

    def location(self, item):
        return reverse("proyecto", args=[item.slug])


class GuiasSitemap(Sitemap):
    def items(self):
        return list(contenido().guias)

    def location(self, item):
        return reverse("guia", args=[item.slug])

    def lastmod(self, item):
        return item.actualizada or item.fecha


SITEMAPS = {"paginas": PaginasSitemap, "proyectos": ProyectosSitemap, "guias": GuiasSitemap}
