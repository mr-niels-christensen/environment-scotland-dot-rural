SHELL := /bin/bash

MAJORMINOR := 0.8

RDFLIBAPPENGINEVERSION := 1.2

PYTHON_FILES := $(shell find src -name "*.py")
FRONTEND_FILES := $(shell find src/main/frontend -name "*.*")
VERSION := $(MAJORMINOR)
NAME := $(shell grep name src/main/python/setup.py | cut -d "'" -f 2)
DISTFILE := build/$(NAME)-$(VERSION).tar.gz
GAEDIR := build/environment-scotland-$(MAJORMINOR)

all: ide runlocal

.PHONY: runlocal
runlocal: .gaebuild.made .pip.for.ide.made test
	source .venv.for.ide/bin/activate && dev_appserver.py $(GAEDIR) --log_level debug

.PHONY: runclean
runclean: .gaebuild.made .pip.for.ide.made test
	source .venv.for.ide/bin/activate && dev_appserver.py $(GAEDIR) --log_level debug --clear_datastore true --clear_search_indexes

.PHONY: gaebuild
gaebuild: .gaebuild.made

.gaebuild.made: .gaebuild.yamls.made .gaebuild.python.made .gaebuild.pip.made .gaebuild.frontend.made
	touch .gaebuild.made

.gaebuild.pip.made: .gaedir.made
	curl --location https://github.com/mr-niels-christensen/rdflib-appengine/releases/download/$(RDFLIBAPPENGINEVERSION)/rdflib-appengine-$(RDFLIBAPPENGINEVERSION).tar.gz > build/rdflib-appengine-$(RDFLIBAPPENGINEVERSION).tar.gz
	pip install -t $(GAEDIR) build/rdflib-appengine-$(RDFLIBAPPENGINEVERSION).tar.gz
	touch .gaebuild.pip.made

.gaebuild.python.made: $(PYTHON_FILES) .gaedir.made
	cp -r src/main/python/* $(GAEDIR)/
	touch .gaebuild.python.made

.gaebuild.frontend.made: $(FRONTEND_FILES) .gaedir.made
	cp -r src/main/frontend $(GAEDIR)/
	touch .gaebuild.frontend.made

.gaebuild.yamls.made: src/main/app.yaml src/main/cron.yaml src/main/appengine_config.py .gaedir.made
	cp src/main/*.yaml $(GAEDIR)/
	cp src/main/appengine_config.py $(GAEDIR)/
	touch .gaebuild.yamls.made

.gaedir.made:
	mkdir -p $(GAEDIR)
	touch .gaedir.made

.PHONY: test
test: .python.test.made

.python.test.made: .pip.for.use.made
	source .venv.for.use/bin/activate && python -m unittest discover -s src/test/python/dot/
	touch .python.test.made

.pip.for.use.made: $(DISTFILE) .venv.for.use/bin/activate
	source .venv.for.use/bin/activate && pip install $(DISTFILE) && pip install --force-reinstall --no-deps --upgrade $(DISTFILE)
	touch .pip.for.use.made

.PHONY: build
build: $(DISTFILE)

$(DISTFILE): $(PYTHON_FILES)
	echo "VERSION = '$(VERSION)'" > src/main/python/dotruralsepake/__init__.py
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
	rm -rf build || true    
	mkdir build

.PHONY: distclean
distclean:
	rm .*.made || true
	rm $(DISTFILE) || true

