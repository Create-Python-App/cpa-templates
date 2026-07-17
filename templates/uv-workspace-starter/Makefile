.PHONY: help sync lint format typecheck test check build clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Install the whole workspace (all members) into .venv
	uv sync

lint: ## Lint every member with Ruff
	uv run ruff check .

format: ## Auto-format the workspace with Ruff
	uv run ruff format .

typecheck: ## Type-check every member with Pyright + mypy
	uv run pyright
	uv run mypy

test: ## Run the test suite across all members
	uv run pytest

check: lint typecheck test ## Run lint + typecheck + tests

build: ## Build wheels/sdists for every workspace member
	uv build --all-packages

clean: ## Remove build artifacts and caches
	rm -rf .venv **/dist **/*.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
