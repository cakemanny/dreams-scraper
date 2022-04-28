PYTHON ?= python3

venv: requirements.txt requirements-test.txt
	$(PYTHON) -m venv venv
	touch -t 01010000 venv
	venv/bin/pip install --upgrade pip setuptools
	venv/bin/pip install --upgrade -r requirements-test.txt
	touch venv

test: venv
	venv/bin/pytest

lint: venv
	venv/bin/flake8 fastclasses_json

.PHONY: clean
clean:
	@echo "you haven't written this step"

run: venv
	venv/bin/python scraper.py

push:
	git add README.md
	git commit -m "Live for Dreams" --author="Dream Bot <actions@users.noreply.github.com>" || true
	git push
