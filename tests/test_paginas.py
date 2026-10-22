import pytest
from django.core.management import call_command

from apps.contenido.cargador import contenido


@pytest.mark.parametrize("url", ["/", "/proyectos/", "/guias/", "/sobre-mi/", "/foro/", "/campus/"])
def test_paginas_principales(client, url):
    r = client.get(url)
    assert r.status_code == 200
    assert "Tu Tiendita" in r.content.decode()


def test_todas_las_fichas_y_guias_responden(client):
    c = contenido()
    for p in c.proyectos:
        r = client.get(f"/proyectos/{p.slug}/")
        assert r.status_code == 200, p.slug
        assert p.nombre in r.content.decode()
    for g in c.guias:
        r = client.get(f"/guias/{g.slug}/")
        assert r.status_code == 200, g.slug
        assert g.titulo in r.content.decode()


def test_el_software_de_escritorio_enlaza_a_github_releases(client):
    html = client.get("/proyectos/omnisuite-studio/").content.decode()
    assert "https://github.com/serranicolasp2-sudo/OmniSuite-Studio/releases/latest" in html
    assert "/releases/latest" not in client.get("/proyectos/tu-cancion/").content.decode()


def test_inexistentes_dan_404(client):
    assert client.get("/proyectos/no-existe/").status_code == 404
    r = client.get("/guias/no-existe/")
    assert r.status_code == 404 and "Esta página no existe" in r.content.decode()


def test_sitemap_robots_feed_y_salud(client):
    sitemap = client.get("/sitemap.xml").content.decode()
    assert "/proyectos/transcriptor-local/" in sitemap and "/guias/videos-a-60-fps-con-ffmpeg/" in sitemap
    assert "Sitemap: http://testserver/sitemap.xml" in client.get("/robots.txt").content.decode()
    assert "Videos a 60 FPS con FFmpeg" in client.get("/guias/feed/").content.decode()
    assert client.get("/salud/").json() == {"status": "ok", "proyectos": 11, "guias": 2}


def test_cabeceras_de_seguridad(client):
    r = client.get("/")
    assert "default-src 'self'" in r["Content-Security-Policy"]
    assert r["X-Frame-Options"] == "DENY"
    assert r["X-Content-Type-Options"] == "nosniff"


def test_contacto_vacio_no_se_muestra(client, settings):
    settings.CONTACTO = {**settings.CONTACTO, "whatsapp": ""}
    assert "wa.me" not in client.get("/").content.decode()
    settings.CONTACTO = {**settings.CONTACTO, "whatsapp": "5491112345678"}
    assert "https://wa.me/5491112345678" in client.get("/").content.decode()


def test_comando_validar_contenido(capsys):
    call_command("validar_contenido")
    assert "Contenido OK: 11 proyectos, 2 guías" in capsys.readouterr().out


def test_favicon_ico_redirige_al_svg(client):
    r = client.get("/favicon.ico")
    assert r.status_code == 301 and r["Location"].endswith("img/favicon.svg")
