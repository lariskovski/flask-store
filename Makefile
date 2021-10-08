SHELL := /bin/bash
.ONESHELL:

setup:
	pip install pip --upgrade
	pip install -r requirements.txt

run: setup
	python src/app.py

test:
	echo test

lint:
	flake8

clean:
	rm src/data.db
