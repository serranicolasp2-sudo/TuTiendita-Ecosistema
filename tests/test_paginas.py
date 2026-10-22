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


def test_botones_de_descarga(client):
    html = client.get("/proyectos/transcriptor-local/").content.decode()
    base = "https://github.com/serranicolasp2-sudo/Transcriptor-Local/releases/latest/download/"
    assert base + "Transcriptor_Instalador_1.0.exe" in html and base + "Transcriptor_Portable.zip" in html
    assert "Descargar instalador · 1,7 GB" in html and "Windows protegió su PC" in html
    # Las apps de video se bajan con OmniSuite, y un servicio no tiene descargas.
    assert (
        "Se descarga con OmniSuite Studio" in client.get("/proyectos/omniflow-fps-booster/").content.decode()
    )
    assert "releases/latest" not in client.get("/proyectos/tu-cancion/").content.decode()


def test_instagram_de_las_marcas_y_personal(client):
    assert "https://instagram.com/tucancion.com.ar" in client.get("/proyectos/tu-cancion/").content.decode()
    assert (
        "https://instagram.com/restauraciondefotos"
        in client.get("/proyectos/restauracion-de-fotos/").content.decode()
    )
    assert "@_nicochapu" in client.get("/sobre-mi/").content.decode()


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
    assert (
        "wa.me" not in client.get("/").content.decode()
        and "wa.me" not in client.get("/sobre-mi/").content.decode()
    )
    settings.CONTACTO = {**settings.CONTACTO, "whatsapp": "5491112345678"}
    assert "https://wa.me/5491112345678" in client.get("/").content.decode()


def test_comando_validar_contenido(capsys):
    call_command("validar_contenido")
    assert "Contenido OK: 11 proyectos, 2 guías" in capsys.readouterr().out


def test_favicon_ico_redirige_al_svg(client):
    r = client.get("/favicon.ico")
    assert r.status_code == 301 and r["Location"].endswith("img/favicon.svg")


def test_ninguna_pagina_publica_datos_personales_del_cv(client):
    """El CV trae DNI, fecha de nacimiento, dirección y teléfonos de referencias: nada de eso va al sitio.
    (El WhatsApp y el mail de Nicolás sí: los autorizó él.)"""
    sensibles = ["35.630.975", "35630975", "24/01/1991", "Debenedetti", "Sarandí", "3077-3769", "5870-1082"]
    urls = ["/", "/sobre-mi/", "/proyectos/", "/guias/", "/foro/", "/campus/"]
    urls += [f"/proyectos/{p.slug}/" for p in contenido().proyectos]
    for url in urls:
        html = client.get(url).content.decode()
        assert not [s for s in sensibles if s in html], url


def test_contacto_y_retrato_en_sobre_mi(client):
    html = client.get("/sobre-mi/").content.decode()
    assert "https://wa.me/5491166912647" in html and "mailto:serranicolas.p@gmail.com" in html
    assert "img/nicolas-serra.webp" in html and 'alt="Foto de Nicolás Serra"' in html
    campus = client.get("/campus/").content.decode()
    assert "wa.me/5491166912647?text=Hola%20Nico" in campus
