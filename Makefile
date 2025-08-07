# Makefile para mBot Voice Assistant

.PHONY: help install test run clean lint format

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
SRC_DIR := src
TEST_DIR := tests
TOOLS_DIR := tools

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias y configurar entorno
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt
	@echo "✅ Entorno configurado. Actívalo con: source $(VENV)/bin/activate"

install-dev: install ## Instalar dependencias de desarrollo
	./$(VENV)/bin/pip install pytest black flake8 mypy
	@echo "✅ Dependencias de desarrollo instaladas"

test: ## Ejecutar todos los tests
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-unit: ## Ejecutar solo tests unitarios
	$(PYTHON) -m pytest $(TEST_DIR)/unit -v

test-integration: ## Ejecutar solo tests de integración
	$(PYTHON) -m pytest $(TEST_DIR)/integration -v

run: ## Ejecutar el asistente principal
	$(PYTHON) main.py

run-minimal: ## Ejecutar test mínimo de conectividad
	$(PYTHON) $(TEST_DIR)/unit/test_connection.py

diagnose: ## Ejecutar herramientas de diagnóstico
	$(PYTHON) $(TOOLS_DIR)/diagnostics/diagnose_loop.py

format: ## Formatear código con black
	black $(SRC_DIR) $(TEST_DIR) $(TOOLS_DIR) *.py

lint: ## Analizar código con flake8
	flake8 $(SRC_DIR) $(TEST_DIR) $(TOOLS_DIR) *.py

type-check: ## Verificar tipos con mypy
	mypy $(SRC_DIR)

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/

setup-ollama: ## Configurar Ollama y descargar modelo
	@echo "Verificando Ollama..."
	@command -v ollama >/dev/null 2>&1 || { echo "Ollama no está instalado. Instálalo desde https://ollama.ai/"; exit 1; }
	ollama pull qwen2.5:7b
	@echo "✅ Modelo Qwen2.5 descargado"

check-system: ## Verificar que todo esté configurado correctamente
	@echo "🔍 Verificando sistema..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "❌ Python3 no encontrado"; exit 1; }
	@command -v ollama >/dev/null 2>&1 || { echo "❌ Ollama no encontrado"; exit 1; }
	@test -f requirements.txt || { echo "❌ requirements.txt no encontrado"; exit 1; }
	@test -f config.py || { echo "❌ config.py no encontrado (copia config_example.py)"; exit 1; }
	@echo "✅ Sistema configurado correctamente"

demo: ## Ejecutar demo rápido del sistema
	@echo "🎬 Ejecutando demo del sistema..."
	$(PYTHON) $(TEST_DIR)/integration/test_complete_system.py

project-stats: ## Mostrar estadísticas del proyecto
	@echo "📊 Estadísticas del proyecto:"
	@echo "Archivos Python: $$(find . -name '*.py' | wc -l)"
	@echo "Líneas de código: $$(find . -name '*.py' -exec wc -l {} + | tail -1)"
	@echo "Tests: $$(find $(TEST_DIR) -name 'test_*.py' | wc -l)"
	@echo "Herramientas: $$(find $(TOOLS_DIR) -name '*.py' | wc -l)"

install-system-deps: ## Instalar dependencias del sistema (macOS)
	@echo "📦 Instalando dependencias del sistema..."
	@command -v brew >/dev/null 2>&1 || { echo "❌ Homebrew requerido en macOS"; exit 1; }
	brew install portaudio ffmpeg
	@echo "✅ Dependencias del sistema instaladas"

full-setup: install-system-deps install setup-ollama check-system ## Configuración completa del proyecto
	@echo "🎉 ¡Configuración completa terminada!"
	@echo "Ejecuta 'make run' para iniciar el asistente"
