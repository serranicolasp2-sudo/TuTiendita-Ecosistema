import urllib.error
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.contenido.cargador import ContenidoInvalido, leer_contenido


class Command(BaseCommand):
    help = "Lee todo contenido/ y avisa si algún proyecto o guía tiene un error. El deploy lo corre antes de publicar."

    def add_arguments(self, parser):
        parser.add_argument(
            "--descargas",
            action="store_true",
            help="Además, prueba que cada botón de descarga lleve a un archivo que existe (necesita internet).",
        )

    def handle(self, *args, **options):
        try:
            c = leer_contenido(settings.CONTENIDO_DIR)
        except ContenidoInvalido as e:
            raise CommandError(str(e)) from e
        self.stdout.write(self.style.SUCCESS(f"Contenido OK: {len(c.proyectos)} proyectos, {len(c.guias)} guías"))
        if options["descargas"]:
            self._probar_descargas(c)

    def _probar_descargas(self, c):
        rotas = []
        for p in c.proyectos:
            for d in p.descargas:
                url = d.url if d.url.startswith("https://") else settings.SITE_URL + d.url
                # GET del primer byte, no HEAD: GitHub firma las direcciones de los archivos solo para GET
                # (un HEAD da 401 aunque el archivo exista). Content-Range trae el tamaño total.
                pedido = urllib.request.Request(url, headers={"User-Agent": "tutiendita-ia.store", "Range": "bytes=0-0"})
                try:
                    with urllib.request.urlopen(pedido, timeout=20) as r:
                        tamano = int((r.headers.get("Content-Range") or "/0").rsplit("/", 1)[1] or 0)
                    self.stdout.write(f"  OK   {p.slug} · {d.nombre}: {tamano / 2**30:.2f} GB")
                except (urllib.error.URLError, TimeoutError) as e:
                    rotas.append(f"{p.slug} · {d.nombre}: {url} ({e})")
        if rotas:
            raise CommandError("Descargas que no responden:\n  " + "\n  ".join(rotas))
        self.stdout.write(self.style.SUCCESS("Descargas OK"))
