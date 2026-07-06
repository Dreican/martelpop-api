# Compose files
COMPOSE_DEV=podman-compose -f compose.yml -f compose.dev.yml
COMPOSE_PROD=podman-compose -f compose.yml -f compose.prod.yml

.PHONY: \
	up down clean restart logs ps shell \
	build rebuild install reset-db \
	migrate revision downgrade \
	test lint format \
	prod-up prod-down \
	prune

# =========================
# Development
# =========================

up:
	$(COMPOSE_DEV) up --build

down:
	$(COMPOSE_DEV) down

clean:
	$(COMPOSE_DEV) down -v --remove-orphans

restart: down up

logs:
	$(COMPOSE_DEV) logs -f

ps:
	$(COMPOSE_DEV) ps

shell:
	$(COMPOSE_DEV) exec api sh

build:
	$(COMPOSE_DEV) build

rebuild:
	$(COMPOSE_DEV) build --no-cache

install:
	pip install -r requirements.txt

reset-db:
	$(COMPOSE_DEV) down -v
	$(COMPOSE_DEV) up --build

# =========================
# Database
# =========================

migrate:
	$(COMPOSE_DEV) exec api alembic upgrade head

revision:
	$(COMPOSE_DEV) exec api alembic revision --autogenerate -m "$(m)"

downgrade:
	$(COMPOSE_DEV) exec api alembic downgrade -1

# =========================
# Quality
# =========================

test:
	$(COMPOSE_DEV) exec api pytest

lint:
	$(COMPOSE_DEV) exec api ruff check .

format:
	$(COMPOSE_DEV) exec api ruff format .

# =========================
# Production
# =========================

prod-up:
	$(COMPOSE_PROD) up -d

prod-down:
	$(COMPOSE_PROD) down

# =========================
# Podman
# =========================

prune:
	podman system prune -f