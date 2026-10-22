.PHONY: run test lint fmt check
run:   ; python manage.py runserver
test:  ; pytest
lint:  ; ruff check . && ruff format --check .
fmt:   ; ruff check --fix . && ruff format .
check: ; python manage.py check && python manage.py validar_contenido
