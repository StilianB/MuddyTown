# Makefile for Muddy Town testing
# Version 1.0.1
all: processtown test

processtown:
	python3 processtown.py $(ARGS)

run: processtown

setup: requirements.txt
	pip install -r requirements.txt

test:
	./test.sh

