SHELL := /bin/bash
all: .pythonrun.made

PYTHON_FILES = $(shell find src -name "*.py")

.PHONY: foo
foo:
	echo $(PYTHON_FILES)

.pythonrun.made: .venv/bin/activate .install.deps.made $(PYTHON_FILES)
	source .venv/bin/activate && cd src/main/python/ && python dot/rural/sepake/ukeof.py
	touch .pythonrun.made

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
    
