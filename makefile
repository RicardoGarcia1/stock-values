# Variables
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
UVICORN := $(VENV_DIR)/bin/uvicorn
APP := app.main:app

# Crear entorno virtual si no existe
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Instalar dependencias si no están instaladas
.install-deps: $(VENV_DIR) requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch .install-deps

# Crear entorno virtual manualmente
venv: $(VENV_DIR)
	@echo "Entorno virtual creado en $(VENV_DIR)"

# Instalar dependencias manualmente
deps: .install-deps
# Ejecutar tests (auto-hace venv y deps)
test: .install-deps
	$(PYTHON) -m pytest

# Correr FastAPI app
run: .install-deps
	$(UVICORN) $(APP) --reload --host '127'.0.0.1 --port 8000

# Activar entorno manualmente
activate:
	@echo "source $(VENV_DIR)/bin/activate"

# Eliminar entorno y marker de dependencias
clean:
	rm -rf $(VENV_DIR) .install-deps
	@echo "Entorno virtual y dependencias eliminados"

# Reinstalar todo desde cero
reset: clean test

.PHONY: venv deps test run activate clean reset

clean-cache:
	@echo "🧹 Eliminando archivos temporales y cachés..."
	find . -type d -name "__pycache__" -exec rm -rf {} + || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + || true
	rm -rf .coverage htmlcov coverage.xml || true
	rm -rf build dist *.egg-info || true
	@echo "✅ Cachés eliminadas."

add-init:
	@echo "📦 Creando __init__.py donde no exista..."
	find app -type d \
		-not -path "*/data*" \
		-not -path "*/__pycache__*" \
		-exec sh -c 'if [ ! -f "$$0/__init__.py" ]; then echo "→ $$0/__init__.py"; touch "$$0/__init__.py"; fi' {} \;
	@echo "✅ Archivos __init__.py creados correctamente."

create-zip:
	docker build -t lambda-fastapi .
	docker create --name extract lambda-fastapi
	docker cp extract:/var/task/lambda.zip ./lambda.zip
	docker rm extract