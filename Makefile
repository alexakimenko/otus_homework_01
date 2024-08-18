# Имя виртуального окружения Poetry
POETRY_RUN = poetry run

# Определение целей

.PHONY: install
install:
	@poetry install

.PHONY: lint
lint: lint-black lint-isort lint-flake8 lint-mypy

.PHONY: lint-black
lint-black:
	@$(POETRY_RUN) black --check .

.PHONY: lint-isort
lint-isort:
	@$(POETRY_RUN) isort --check-only .

.PHONY: lint-flake8
lint-flake8:
	@$(POETRY_RUN) flake8 .

.PHONY: lint-mypy
lint-mypy:
	@$(POETRY_RUN) mypy .

.PHONY: test
test:
	@$(POETRY_RUN) pytest tests/

.PHONY: run
run:
	@$(POETRY_RUN) python src/app/log_analyzer.py --config config.yaml

.PHONY: format
format: format-black format-isort

.PHONY: format-black
format-black:
	@$(POETRY_RUN) black .

.PHONY: format-isort
format-isort:
	@$(POETRY_RUN) isort .

.PHONY: coverage
coverage:
	@$(POETRY_RUN) pytest --cov=src --cov-report=html tests/

.PHONY: clean
clean:
	@rm -rf .pytest_cache
	@rm -rf __pycache__
	@rm -rf htmlcov
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete