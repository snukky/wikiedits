PYTHON = python3
SHELL = /bin/bash

all: setup test

setup:
	pip3 install -r requirements.txt
	$(PYTHON) -c "import nltk; nltk.download('punkt')"

test:
	nosetests

.PHONY: all setup test
