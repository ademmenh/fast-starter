PYTHON   = python3
APP_DIR  = .
APP      = src.main:app
HOST     = 0.0.0.0
PORT     = 8000
WORKERS  = 4

# Find uv command - use which to locate it, fall back to known path
UV_CMD = $(shell which uv 2>/dev/null || echo /home/gon/.local/bin/uv)
UV_RUN = $(UV_CMD) run

PYTEST  = $(UV_RUN) pytest
UVICORN = $(UV_RUN) uvicorn
RUFF    = $(UV_RUN) ruff

.DEFAULT_GOAL := help

CYAN  = \033[0;36m
RESET = \033[0m

.PHONY: help \
        build\:dev build\:prod \
        start\:dev stop\:dev \
        attach \
        test test\:unit test\:integration test\:e2e \
        lint format clean \
        migrate shell ps

# ── Help ───────────────────────────────────────────────────────────────────────
help:
	@echo -e "$(CYAN)Restaurant API — available commands$(RESET)"
	@echo -e "  Local"
	@echo -e "    $(CYAN)make setup$(RESET)              Create virtual environment"
	@echo -e "    $(CYAN)make deps$(RESET)               Install all dependencies (runtime + dev)"
	@echo -e "    $(CYAN)make lint$(RESET)               Check code style (ruff)"
	@echo -e "    $(CYAN)make format$(RESET)             Auto-format code (ruff)"
	@echo -e "    $(CYAN)make clean$(RESET)              Remove venv and caches"
	@echo -e "  Docker"
	@echo -e "    $(CYAN)make build:dev$(RESET)          Build development image"
	@echo -e "    $(CYAN)make build:prod$(RESET)         Build production image"
	@echo -e "    $(CYAN)make start:dev$(RESET)          Start dev stack (hot-reload, detached)"
	@echo -e "    $(CYAN)make stop:dev$(RESET)           Stop  dev stack"
	@echo -e "    $(CYAN)make attach$(RESET)             Tail live app logs"
	@echo -e "    $(CYAN)make migrate$(RESET)            Run Alembic migrations in dev container"
	@echo -e "    $(CYAN)make shell$(RESET)              Open shell in running dev container"
	@echo -e "    $(CYAN)make ps$(RESET)                 Show running containers"
	@echo -e "  Tests"
	@echo -e "    $(CYAN)make test$(RESET)               Run all tests"
	@echo -e "    $(CYAN)make test:unit$(RESET)          Unit tests only"
	@echo -e "    $(CYAN)make test:integration$(RESET)   Integration tests only"
	@echo -e "    $(CYAN)make test:e2e$(RESET)           End-to-end tests only"
	@echo -e ""

# ── Docker ─────────────────────────────────────────────────────────────────────
build\:dev:
	docker compose -f docker-compose.dev.yml build

build\:prod:
	docker compose build

start\:dev:
	docker compose -f docker-compose.dev.yml up -d

stop\:dev:
	docker compose -f docker-compose.dev.yml down

attach:
	docker compose -f docker-compose.dev.yml logs -f app

migrate:
	docker compose -f docker-compose.dev.yml exec app alembic upgrade head

shell:
	docker compose -f docker-compose.dev.yml exec app /bin/bash

ps:
	docker compose -f docker-compose.dev.yml ps

# ── Tests ──────────────────────────────────────────────────────────────────────
test:
	$(PYTEST) src/ -v

test\:unit:
	$(PYTEST) src/ -v -k unit

test\:integration:
	$(PYTEST) src/ -v -k integration

test\:e2e:
	$(PYTEST) src/ -v -k e2e

# ── Code quality ───────────────────────────────────────────────────────────────
lint:
	$(RUFF) check src

format:
	$(RUFF) check --fix src
	$(RUFF) format src

# ── Cleanup ────────────────────────────────────────────────────────────────────
clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache"  -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "$(CYAN)Cleaned$(RESET)"