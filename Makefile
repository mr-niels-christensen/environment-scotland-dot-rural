.PHONY: test
test:
	python -m unittest discover -s src/test/python/dot/ #TODO: Set up after refactoring

.PHONY: deploy
deploy:
	@head -2 src/main/app.yaml
	@read -p "Press RETURN to deploy the above, CTRL+C to cancel"
	appcfg.py update src/main/
