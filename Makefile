SHELL := /bin/bash
.ONESHELL:

all: run
	@echo "All good."

setup:
	pip install -r requirements.txt
	python src/create_tables.py

run: clean setup
	python src/app.py

test:
	echo test

clean:
	rm data.db