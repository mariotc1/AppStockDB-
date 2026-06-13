.PHONY: up down build logs api-logs db-logs shell-api shell-db run test lint clean

COMPOSE      = docker compose -f docker/docker-compose.yml
COMPOSE_PROD = $(COMPOSE) -f docker/docker-compose.prod.yml

# ── Desarrollo local ───────────────────────────────────────────────────────────

up:          ## Levanta MySQL + API + Adminer en segundo plano
	$(COMPOSE) up -d --build

down:        ## Para y elimina los contenedores (datos persistidos en volúmenes)
	$(COMPOSE) down

build:       ## Reconstruye la imagen de la API sin caché
	$(COMPOSE) build --no-cache api

logs:        ## Logs de todos los servicios en tiempo real
	$(COMPOSE) logs -f

api-logs:    ## Logs solo de la API
	$(COMPOSE) logs -f api

db-logs:     ## Logs solo de MySQL
	$(COMPOSE) logs -f db

shell-api:   ## Shell dentro del contenedor de la API
	$(COMPOSE) exec api bash

shell-db:    ## Cliente MySQL dentro del contenedor de la BD
	$(COMPOSE) exec db mysql -u root -p${DB_ROOT_PASSWORD:-rootpassword} ${DB_NAME:-db_inmuebles}

# ── Escritorio ─────────────────────────────────────────────────────────────────

run:         ## Arranca la app de escritorio PyQt5 (requiere contenedores activos)
	python launcher.py

# ── Producción ─────────────────────────────────────────────────────────────────

prod-up:     ## Levanta en modo producción (4 workers, Adminer solo en maintenance)
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

# ── Calidad ────────────────────────────────────────────────────────────────────

test:        ## Ejecuta los tests (unit, sin BD)
	pytest tests/ -v -m "not integration"

lint:        ## Comprueba estilo con flake8
	flake8 backend/ frontend/ --max-line-length=120 --extend-ignore=E501,W503,E402

# ── Empaquetado ────────────────────────────────────────────────────────────────

package:     ## Empaqueta el escritorio con PyInstaller (requiere .env con URL de producción)
	pyinstaller launcher.spec

# ── Limpieza ───────────────────────────────────────────────────────────────────

clean:       ## Elimina build/, dist/ y __pycache__
	rm -rf build/ dist/ **/__pycache__ *.pyc

help:        ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*##' Makefile | \
	  awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
