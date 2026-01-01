VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

set_up:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run_test:
	$(PYTHON) -m pytest tests
