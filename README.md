Wiki Edits 2.0
==============

A collection of scripts for automatic extraction of edited sentences from text
edition histories, such as Wikipedia revisions. It was used to create
the [WikEd Error Corpus](http://romang.home.amu.edu.pl/wiked/wiked.html) --- a
corpus of corrective Wikipedia edits:

This is a new version of the library and it is **not compatible** with the old
version! Back to commit 163d771 if you need old scripts.

Requirements
------------

This package is tested on Ubuntu with Python 2.7.

Required python packages:

- `nltk` with NLTK data _punkt_, see: http://www.nltk.org/
- `Levenshtein`, see: https://pypi.python.org/pypi/python-Levenshtein/

Optional packages:

- `pyyaml`, see: http://pyyaml.org/
- `joblib`, see: https://pypi.python.org/pypi/joblib
- `nose`, see: https://nose.readthedocs.org/en/latest/

Run tests by typing `nosetests` from main directory.

Installation
------------

Installation of all requirements is possible via Makefile if you have `pip`
installed:

    sudo apt-get install python-pip
    sudo make all

Usage
-----

Example usage from main directory:

    ./bin/txt_edits.py tests/data/lorem_ipsum.old.txt tests/data/lorem_ipsum.new.txt

And with Wikipedia dump file:

    zcat tests/data/enwiki-20140102.tiny.xml.gz | ./bin/wiki_edits.py

The last script in the `bin` directory can be run with a list of dump files or
URLs:

    ./bin/collect_wiki_edits.py -w /path/to/work/dir dumplist.txt

Language-specific options
-------------------------

All scripts are mostly language-independent. A few components need to be
checked or updated to run these scripts for non-English languages:

- model for NLTK _punkt_ tokenizer, 
  see: https://github.com/nltk/nltk_data/tree/gh-pages
- regular expressions for filtering reverted revisions,
  see file: `wikiedits/wiki/__init__.py`
- list of supported languages,
  see file: `wikiedits/__init__.py`

Currently supported languages: English, Polish.
