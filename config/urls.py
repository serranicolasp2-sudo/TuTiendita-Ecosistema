from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.contenido.sitemaps import SITEMAPS

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.contenido.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="sitemap"),
]
