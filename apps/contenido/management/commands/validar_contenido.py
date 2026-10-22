from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.contenido.cargador import ContenidoInvalido, leer_contenido


class Command(BaseCommand):
    help = "Lee todo contenido/ y avisa si algún proyecto o guía tiene un error. El deploy lo corre antes de publicar."

    def handle(self, *args, **options):
        try:
            c = leer_contenido(settings.CONTENIDO_DIR)
        except ContenidoInvalido as e:
            raise CommandError(str(e)) from e
        self.stdout.write(
            self.style.SUCCESS(f"Contenido OK: {len(c.proyectos)} proyectos, {len(c.guias)} guías")
        )
