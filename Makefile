SHELL := /bin/bash

MAJORMINOR := 0.5

PYTHON_FILES := $(shell find src -name "*.py")
FRONTEND_FILES := $(shell find src/main/frontend -name "*.*")
MICROVERSION := $(shell date "+%Y%m%d%H%M%S")
VERSION := $(MAJORMINOR).$(MICROVERSION)
NAME := $(shell grep name src/main/python/setup.py | cut -d "'" -f 2)
DISTFILE := build/$(NAME)-$(VERSION).tar.gz
GAEDIR := build/environment-scotland-$(MAJORMINOR)

all: ide data frontend

.PHONY: runlocal
runlocal: .gaebuild.made .pip.for.ide.made 
	source .venv.for.ide/bin/activate && dev_appserver.py $(GAEDIR) --log_level debug

.PHONY: runclean
runclean: .gaebuild.made .pip.for.ide.made 
	source .venv.for.ide/bin/activate && dev_appserver.py $(GAEDIR) --log_level debug --clear_datastore true

.PHONY: gaebuild
gaebuild: .gaebuild.made

.gaebuild.made: $(GAEDIR)/appengine/ndbstore.py .gaebuild.yamls.made .gaebuild.python.made $(GAEDIR)/rdflib/__init__.py .gaebuild.frontend.made
	touch .gaebuild.made

$(GAEDIR)/rdflib/__init__.py: .gaedir.made
	pip install -t $(GAEDIR) rdflib

.gaebuild.python.made: $(PYTHON_FILES) .gaedir.made
	cp -r src/main/python/* $(GAEDIR)/
	touch .gaebuild.python.made

.gaebuild.frontend.made: $(FRONTEND_FILES) .gaedir.made
	cp -r src/main/frontend $(GAEDIR)/
	touch .gaebuild.frontend.made

.gaebuild.yamls.made: src/main/app.yaml src/main/cron.yaml .gaedir.made
	cp src/main/*.yaml $(GAEDIR)/
	touch .gaebuild.yamls.made

$(GAEDIR)/appengine/ndbstore.py: .gaedir.made
	mkdir -p $(GAEDIR)/appengine/
	touch $(GAEDIR)/appengine/__init__.py
	curl https://raw.githubusercontent.com/mr-niels-christensen/rdflib-appengine/master/appengine/ndbstore.py > $(GAEDIR)/appengine/ndbstore.py

.gaedir.made:
	mkdir -p $(GAEDIR)
	touch .gaedir.made

.PHONY: frontend
frontend: .frontend.made

.frontend.made: $(FRONTEND_FILES)
	rm -rf /srv/www/alpha/ || true
	mkdir /srv/www/alpha/
	cp -r src/main/frontend/* /srv/www/alpha/
	touch .frontend.made

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
	echo "VERSION = '$(VERSION)'" > src/main/python/dot/__init__.py
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
	rm -rf build || true    
	mkdir build
