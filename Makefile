.PHONY: setup dev test lint format migrate seed evaluate clean docker-build

PYTHON ?= python

setup:
	$(PYTHON) -m pip install -e ".[dev]"

dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

worker:
	celery -A app.workers.celery_app worker --loglevel=info --concurrency=4

beat:
	celery -A app.workers.celery_app beat --loglevel=info

migrate:
	alembic upgrade head

migrate-create:
	alembic revision --autogenerate -m "$(name)"

seed:
	$(PYTHON) -m seed.seed_runner

test:
	pytest -v --cov=app tests/

test-unit:
	pytest -v tests/unit/

test-integration:
	pytest -v tests/integration/

test-security:
	pytest -v tests/security/

test-rag:
	pytest -v tests/rag/

test-e2e:
	pytest -v tests/e2e/

evaluate:
	$(PYTHON) -m app.evaluation.runner

lint:
	ruff check .
	mypy app

format:
	ruff format .
	isort .

docker-up:
	docker compose up -d

docker-down:
	docker compose down -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
