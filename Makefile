SHELL := /bin/bash
all: .python.run.made

PYTHON_FILES = $(shell find src -name "*.py")
VERSION = $(shell grep version src/main/python/setup.py | cut -d "'" -f 2)
NAME = $(shell grep name src/main/python/setup.py | cut -d "'" -f 2)
DISTFILE = build/$(NAME)-$(VERSION).tar.gz

.python.run.made: .venv/bin/activate .install.deps.made $(PYTHON_FILES) test
	source .venv/bin/activate && cd src/main/python/ && python dot/rural/sepake/ukeof.py
	touch .pythonrun.made

.PHONY: test
test: .python.test.made

.python.test.made: .venv-test/bin/activate .install.deps.test.made $(PYTHON_FILES)
	source .venv-test/bin/activate && python -m unittest discover -s src/test/python/dot/
	touch .python.test.made

.PHONY: build
build: $(DISTFILE)

$(DISTFILE): $(PYTHON_FILES)
	(cd src/main/python && ./setup.py sdist --dist-dir ../../../build/)

.venv/bin/activate:
	virtualenv .venv

.venv-test/bin/activate:
	virtualenv .venv-test

.install.deps.made: .venv/bin/activate
	source .venv/bin/activate && pip install rdflib
	touch .install.deps.made

.install.deps.test.made: .venv-test/bin/activate $(DISTFILE)
	source .venv-test/bin/activate && pip install $(DISTFILE)
	touch .install.deps.test.made

.PHONY: clean
clean: distclean
	rm -rf .venv/ || true
	rm -rf .venv-test/ || true

.PHONY: distclean
distclean:
	rm .*.made || true
	rm $(DISTFILE) || true    
