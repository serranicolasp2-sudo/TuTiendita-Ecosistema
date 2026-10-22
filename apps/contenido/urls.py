from django.urls import path

from . import views
from .feeds import GuiasFeed

urlpatterns = [
    path("proyectos/", views.proyectos, name="proyectos"),
    path("proyectos/<slug:slug>/", views.proyecto, name="proyecto"),
    path("guias/", views.guias, name="guias"),
    path("guias/feed/", GuiasFeed(), name="guias_feed"),
    path("guias/<slug:slug>/", views.guia, name="guia"),
]
