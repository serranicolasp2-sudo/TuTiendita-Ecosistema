from django.conf import settings


def sitio(request):
    return {"contacto": settings.CONTACTO, "site_url": settings.SITE_URL, "titular": settings.TITULAR}
