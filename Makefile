SHELL := /bin/bash
all: .python.run.made

PYTHON_FILES = $(shell find src -name "*.py")

.python.run.made: .venv/bin/activate .install.deps.made $(PYTHON_FILES) .python.test.made
	source .venv/bin/activate && cd src/main/python/ && python dot/rural/sepake/ukeof.py
	touch .pythonrun.made

.python.test.made: .venv/bin/activate .install.deps.made $(PYTHON_FILES)
	source .venv/bin/activate && PYTHON_PATH=./src/main/python/ && echo $$PYTHON_PATH && python -m unittest discover -s src/test/python/dot/
	touch .python.test.made

.venv/bin/activate:
	virtualenv .venv

.install.deps.made: .venv/bin/activate
	source .venv/bin/activate && pip install rdflib
	touch .install.deps.made

.PHONY: clean
clean: distclean
	rm -rf .venv/

distclean:
	rm .*.made
    
