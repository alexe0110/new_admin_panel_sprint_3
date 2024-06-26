VENV ?= .venv
LINE_LENGTH ?= 120
LINT_DIRS = .

init:
	python3.11 -m venv .venv
	$(VENV)/bin/pip config --site set global.index-url https://pypi.org/simple/
	$(VENV)/bin/pip config --site set global.extra-index-url https://pypi.org/simple/
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry
	$(VENV)/bin/poetry install


plint:
	$(VENV)/bin/ruff format $(LINT_DIRS)
	$(VENV)/bin/ruff check $(LINT_DIRS) --fix --show-fixes
	$(VENV)/bin/mypy --install-types --non-interactive --namespace-packages \
	    --explicit-package-bases $(LINT_DIRS) --disable-error-code import-untyped \
	    --exclude utils/state --exclude tests


docker-run:
	docker compose up -d --build

local-run:
	docker compose up redis pg_db els -d --build
	$(VENV)/bin/python main.py