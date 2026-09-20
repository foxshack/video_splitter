# Constants
PYTHON_ENV_PATH := .venv
PYTHON := $(PYTHON_ENV_PATH)/bin/python
PRECOMMIT = $(PYTHON_ENV_PATH)/bin/pre-commit

# Targets
.PHONY: help install-precommit uninstall-precommit update-precommit \
	precommit precommit-all test test-cov clean

help:
	@echo "Available commands:"
	@echo "  make install-precommit    - Install pre-commit and set up hooks"
	@echo "  make uninstall-precommit  - Uninstall pre-commit hooks"
	@echo "  make update-precommit     - Update pre-commit hooks to latest versions"
	@echo "  make precommit            - Run pre-commit on staged files"
	@echo "  make precommit-all        - Run pre-commit on all files"
	@echo "  make test                 - Run unit tests"
	@echo "  make test-cov             - Run tests with coverage report"

.venv:
	@if [ ! -d "$(PYTHON_ENV_PATH)" ]; then \
		python3 -m venv $(PYTHON_ENV_PATH); \
		$(PYTHON_ENV_PATH)/bin/pip install --upgrade pip; \
		$(PYTHON_ENV_PATH)/bin/pip install build; \
		echo "Virtual environment created."; \
	fi

install-precommit: .venv
	@$(PYTHON_ENV_PATH)/bin/pip install pre-commit
	@$(PYTHON_ENV_PATH)/bin/pre-commit install
	@echo "Pre-commit installed"

uninstall-precommit: .venv
	@$(PYTHON_ENV_PATH)/bin/pre-commit uninstall

update-precommit: .venv
	@$(PYTHON_ENV_PATH)/bin/pre-commit autoupdate

build: .venv
	$(PYTHON) -m build

test: .venv
	@echo "Installing test dependencies..."
	@$(PYTHON_ENV_PATH)/bin/pip install -e ".[dev]" > /dev/null 2>&1
	@echo "Running tests..."
	@$(PYTHON_ENV_PATH)/bin/pytest -v

test-cov: .venv
	@echo "Installing test dependencies..."
	@$(PYTHON_ENV_PATH)/bin/pip install -e ".[dev]" > /dev/null 2>&1
	@echo "Running tests with coverage..."
	@$(PYTHON_ENV_PATH)/bin/pytest --cov=splitter_cli --cov-report=html --cov-report=term-missing -v
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

precommit:
	pre-commit run

precommit-all:
	pre-commit run --all-files

clean:
	@echo "Cleaning up..."
	@rm -rf build dist *.egg-info
	@rm -rf $(PYTHON_ENV_PATH)
	@echo "Clean up complete"
