# Constants
VENV_NAME ?= .venv
PYTHON_ENV_PATH := $(or $(VIRTUAL_ENV), $(VENV_NAME))
PRECOMMIT = $(PYTHON_ENV_PATH)/bin/pre-commit

# Targets
.PHONY: help install-precommit uninstall-precommit update-precommit precommit precommit-all

help:
	@echo "Available commands:"
	@echo "  make install-precommit    - Install pre-commit and set up hooks"
	@echo "  make uninstall-precommit  - Uninstall pre-commit hooks"
	@echo "  make update-precommit     - Update pre-commit hooks to latest versions"
	@echo "  make precommit            - Run pre-commit on staged files"
	@echo "  make precommit-all        - Run pre-commit on all files"

pip_env:
	@# check if PYTHON_ENV = $(VENV_NAME) and if it is then check whether the directory exists
	@-echo "PYTHON_ENV is set to $(PYTHON_ENV_PATH)";
	@-if [ "$(PYTHON_ENV_PATH)" = $(VENV_NAME) ]; then \
		if [ ! -d "$(PYTHON_ENV_PATH)" ]; then \
			echo "Virtual environment created."; \
			python3 -m venv $(VENV_NAME) && $(VENV_NAME)/bin/pip install --upgrade pip; \
		fi; \
	fi

install-precommit: pip_env
	@$(PYTHON_ENV_PATH)/bin/pip install pre-commit
	@$(PYTHON_ENV_PATH)/bin/pre-commit install
	@echo "Pre-commit installed"

uninstall-precommit: pip_env
	@$(PYTHON_ENV_PATH)/bin/pre-commit uninstall

update-precommit: pip_env
	@$(PYTHON_ENV_PATH)/bin/pre-commit autoupdate

clean:
	@rm -rf $(VENV_NAME)
	@echo "Clean up complete"

precommit:
	pre-commit run

precommit-all:
	pre-commit run --all-files
