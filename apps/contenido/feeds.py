import datetime as dt

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone

from .cargador import contenido


class GuiasFeed(Feed):
    title = "Tu Tiendita IA · Guías paso a paso"
    description = (
        "Cómo se construyen los proyectos de Tu Tiendita IA, explicado para que los puedas replicar."
    )

    def link(self):
        return reverse("guias")

    def items(self):
        return contenido().guias[:20]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return item.resumen

    def item_link(self, item):
        return reverse("guia", args=[item.slug])

    def item_pubdate(self, item):
        return timezone.make_aware(dt.datetime.combine(item.fecha, dt.time(9)))

    def item_author_name(self, item):
        return settings.TITULAR
