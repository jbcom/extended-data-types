PYMODULE := extended_data_types
TESTS := tests

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
	poetry install --with dev

.PHONY: lint
lint: install ## Lint the code using ruff
	poetry run ruff check $(PYMODULE)

.PHONY: test
test: install ## Run tests with coverage report
	poetry run coverage run -m pytest $(TESTS)
	poetry run coverage report -m

.PHONY: ci
ci: lint test ## Run ci battery

.PHONY: clean
clean: ## Clean the repository
	git clean -Xdf

.PHONY: docs-clean
docs-clean: ## Clean the docs directory
	rm -rf docs/_autosummary || echo "No _autosummary directory to cleanup"
	rm -rf docs/_build || echo "No _build directory to cleanup"

.PHONY: docs-autogen
docs-autogen: install docs-clean ## Autogenerate module documentation stubs
	poetry run sphinx-autogen docs/index.rst

.PHONY: docs-readme
docs-readme: docs-autogen ## Generate README.md from a markdown docs build
	poetry run sphinx-build -M markdown docs docs/_build
	cp docs/_build/markdown/index.md README.md

.PHONY: docs-pages
docs-pages: docs-autogen ## Generate GH pages docs from an HTML docs build
	poetry run sphinx-build -M html docs docs/_build

.PHONY: build
build: ## Build the distribution packages
	poetry build
