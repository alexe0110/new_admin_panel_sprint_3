VENV ?= .venv
LINE_LENGTH ?= 120
LINT_DIRS = etl

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
	    --explicit-package-bases $(LINT_DIRS) --disable-error-code import-untyped --exclude movies/migrations


docker-run:
	docker-compose up -d --build
