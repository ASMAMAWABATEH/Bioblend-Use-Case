# Makefile for BioBlend Use Case
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# ------------------------------
# Setup virtual environment
# ------------------------------
set_up:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov

# ------------------------------
# Run unit tests
# ------------------------------
run_test:
	$(PYTHON) -m pytest tests

# ------------------------------
# Run tests with coverage report
# ------------------------------
coverage:
	$(PYTHON) -m pytest --cov=src --cov-report=term --cov-report=xml

# ------------------------------
# Clean temporary files and coverage
# ------------------------------
clean:
	rm -rf $(VENV) __pycache__ *.pyc .pytest_cache htmlcov coverage.xml
