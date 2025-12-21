.PHONY: help install-precommit uninstall-precommit update-precommit precommit precommit-all

help:
	@echo "Available commands:"
	@echo "  make install-precommit    - Install pre-commit and set up hooks"
	@echo "  make uninstall-precommit  - Uninstall pre-commit hooks"
	@echo "  make update-precommit     - Update pre-commit hooks to latest versions"
	@echo "  make precommit            - Run pre-commit on staged files"
	@echo "  make precommit-all        - Run pre-commit on all files"

install-precommit:
	pip install pre-commit
	pre-commit install

uninstall-precommit:
	pre-commit uninstall

update-precommit:
	pre-commit autoupdate

precommit:
	pre-commit run

precommit-all:
	pre-commit run --all-files
