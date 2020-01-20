PYTHON = python3
SHELL = /bin/bash

all: setup test

setup:
	pip3 install -r requirements.txt
	$(PYTHON) -c "import nltk; nltk.download('punkt')"

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

.PHONY: all setup test test-run clean clean-run
