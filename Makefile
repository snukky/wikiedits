PYTHON_27 = python
SHELL = /bin/bash

all: setup test

setup:
	pip install -U nltk
	$(PYTHON_27) -c "import nltk; nltk.download('punkt')"
	pip install python-Levenshtein
	pip install pyyaml
	pip install nose
	pip install joblib

test: 
	nosetests

test-run: tests/data/dumps.txt
	bin/collect_wiki_edits.py -w tests/workdir -e " -l polish" $^

tests/data/dumps.txt: tests/data/enwiki-20140102.tiny.xml.gz
	echo $^ > $@
	cp $^ tests/data/enwiki-20140102.tiny.copy.xml.gz
	echo tests/data/enwiki-20140102.tiny.copy.xml.gz >> $@
	zcat $^ > tests/data/enwiki-20140102.tiny.xml 
	echo tests/data/enwiki-20140102.tiny.xml >> $@


clean-run:
	rm -rf tests/workdir tests/data/enwiki-20140102.tiny.copy.xml.gz tests/data/enwiki-20140102.tiny.xml tests/data/dumps.txt

clean: clean-run
	find . -name "*~" -type f -delete
	find . -name "*.pyc" -type f -delete

.PHONY: all setup test test-run clean clean-run 
