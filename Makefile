.PHONY: setup test lint docs clean

setup:
	uv sync --extra dev --extra plot --extra docs

test:
	uv run pytest

lint:
	uv run ruff check src tests

docs:
	uv run mkdocs build

clean:
	rm -rf .pytest_cache .ruff_cache dist build site
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
