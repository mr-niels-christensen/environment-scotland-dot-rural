SHELL := /bin/bash
all: .pythonrun.made

.pythonrun.made: .venv/bin/activate .install.deps.made src/main/python/dot/rural/sepake/ukeof.py
	source .venv/bin/activate && cd src/main/python/ && python dot/rural/sepake/ukeof.py
	touch .pythonrun.made

.venv/bin/activate:
	virtualenv .venv

.install.deps.made: .venv/bin/activate
	source .venv/bin/activate && pip install rdflib
	touch .install.deps.made

.PHONY: clean
clean:
	rm -rf .venv/
	rm .*.made

    
