all: .pythonrun.made

.pythonrun.made: .venv/bin/activate src/main/python/dot/rural/sepake/ukeof.py
	source .venv/bin/activate && cd src/main/python/ && python dot/rural/sepake/ukeof.py
	touch .pythonrun.made

.venv/bin/activate:
	virtualenv .venv
	source .venv/bin/activate && pip install rdflib

.PHONY: clean
clean:
	rm -rf .venv/
	rm .pythonrun.made

    
