.ONESHELL:

VENV = .venv
PYTHON = $(VENV)/bin/python

# only create .venv if .venv is messing
$(VENV)/bin/python:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -r requirements.txt

#only runs python after making/checking .venv is here
run: $(VENV)/bin/python
	$(PYTHON) __init__.py

#for some reason, if I use "default" instead of "run", the .venv files are checked/installed, but the python file isn't ran
