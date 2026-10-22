import pytest

from apps.contenido import cargador


@pytest.fixture(autouse=True)
def _cache_limpio():
    """Cada test arranca leyendo el contenido de cero (algunos apuntan CONTENIDO_DIR a una carpeta temporal)."""
    cargador._cache.update(firma=None, contenido=None)
    yield
    cargador._cache.update(firma=None, contenido=None)
