SHELL := /bin/bash

PYTHON_FILES = $(shell find src -name "*.py")
VERSION = $(shell grep version src/main/python/setup.py | cut -d "'" -f 2)
NAME = $(shell grep name src/main/python/setup.py | cut -d "'" -f 2)
DISTFILE = build/$(NAME)-$(VERSION).tar.gz

.PHONY: foo
foo:
	FOO=`date "+%Y%m%d%H%M%S"` && echo $$FOO
all: ide data

.PHONY: data
data: .ukeof.data.made .pure.data.made

.ukeof.data.made: test
	source .venv.for.use/bin/activate && import_ukeof.py
	touch .ukeof.data.made

.pure.data.made: test
	source .venv.for.use/bin/activate && import_pure.py
	touch .pure.data.made

.PHONY: test
test: .python.test.made

.python.test.made: .pip.for.use.made
	source .venv.for.use/bin/activate && python -m unittest discover -s src/test/python/dot/
	touch .python.test.made

.pip.for.use.made: $(DISTFILE) .venv.for.use/bin/activate
	source .venv.for.use/bin/activate && pip install $(DISTFILE)
	touch .pip.for.use.made

.PHONY: build
build: $(DISTFILE)

$(DISTFILE): $(PYTHON_FILES)
	(cd src/main/python && ./setup.py sdist --dist-dir ../../../build/)

.venv.for.use/bin/activate:
	virtualenv .venv.for.use

.PHONY: ide
ide: .pip.for.ide.made

.pip.for.ide.made: .venv.for.ide/bin/activate src/main/python/requirements.txt $(PYTHON_FILES)
	source .venv.for.ide/bin/activate && (cd src/main/python && pip install -r requirements.txt)
	touch .pip.for.ide.made

.venv.for.ide/bin/activate:
	virtualenv .venv.for.ide

.PHONY: clean
clean: distclean
	rm -rf .venv*/ || true

.PHONY: distclean
distclean:
	rm .*.made || true
	rm $(DISTFILE) || true    
