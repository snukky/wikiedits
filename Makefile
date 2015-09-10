PYTHON_27 = python

all: setup test

setup:
	pip install -U nltk
	$(PYTHON_27) -c "import nltk; nltk.download('punkt')"
	pip install python-Levenshtein
	pip install pyyaml
	pip install nose

test:
	nosetests

clean:
	find . -name "*~" -type f -delete
	find . -name "*.pyc" -type f -delete
