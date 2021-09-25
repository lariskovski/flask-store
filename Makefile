SHELL := /bin/bash
.ONESHELL:

all: run
	@echo "All good."

setup:
	python3.8 -m venv .
	source bin/activate
	pip install -r requirements.txt
	python create_tables.py

test:
	echo test
