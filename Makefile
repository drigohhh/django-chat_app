.PHONY: install
install:
	poetry install

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit install

.PHONY: uninstall-pre-commit
uninstall-pre-commit:
	poetry run pre-commit uninstall

.PHONY: upd-pre-commit
upd-pre-commit: uninstall-pre-commit install-pre-commit

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m core.manage makemigrations

.PHONY: runserver
runserver:
	poetry run python -m core.manage runserver

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: update
update: install migrations migrate upd-pre-commit
