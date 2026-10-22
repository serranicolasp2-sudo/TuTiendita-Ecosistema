from django.urls import path

from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("sobre-mi/", views.sobre_mi, name="sobre_mi"),
    path("foro/", views.foro, name="foro"),
    path("campus/", views.campus, name="campus"),
    path("robots.txt", views.robots, name="robots"),
    path("salud/", views.salud, name="salud"),
    path("favicon.ico", views.favicon),
]
