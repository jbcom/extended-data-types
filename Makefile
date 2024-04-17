PYMODULE := extended_data_types
TESTS := tests
POETRY := $(shell command -v poetry 2> /dev/null)

.DEFAULT_GOAL := help

.PHONY: all
all: install format lint typecheck test ## Install dependencies, format, lint, typecheck, and run tests

.PHONY: help
help: ## Display this help screen
	@echo "Makefile for managing this project"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@for file in $(MAKEFILE_LIST); do \
	    grep -E '^[a-zA-Z_-]+:.*?## .*$$' $$file; \
	done | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install all dependencies
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
	$(POETRY) run pip install --upgrade pip setuptools
	$(POETRY) install --with dev

.PHONY: format
format: install ## Format the code using autoimport and isort
	$(POETRY) run autoimport $(PYMODULE)
	$(POETRY) run isort .

.PHONY: lint
lint: install ## Lint the code using black
	$(POETRY) run black .

.PHONY: typecheck
typecheck: install ## Typecheck the code using mypy
	$(POETRY) run mypy $(PYMODULE)

.PHONY: test
test: install ## Run tests with coverage report
	$(POETRY) run pytest --cov=$(PYMODULE) --cov-report=term-missing --cov-report=xml:coverage.xml

.PHONY: clean
clean: ## Clean the repository
	git clean -Xdf

.PHONY: future
future: install ## Add future imports to the code
	poetry run python scripts/add_future_imports.py

.PHONY: docs
docs: install ## Generate documentation
	$(POETRY) run sphinx-build -M html docs docs/_build

.PHONY: readme
readme: install ## Generate README.md from README.rst
	$(POETRY) run pandoc README.rst -o README.md

.PHONY: tox
tox: install ## Run tests across multiple Python versions
	$(POETRY) run tox
