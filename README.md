Wiki Edits 2.0
==============

A collection of scripts for automatic extraction of edited sentences from text
edition histories, such as Wikipedia revisions. It was used to build the WikEd
Error Corpus --- a corpus of corrective Wikipedia edits. 

This is a new version of the library and it is *not compatible* with old
version! See branch `oldversion` if you need older scripts.

Requirements
------------

This package is tested on Ubuntu with Python 2.7.

Required python packages:

- `nltk` with NLTK data _punkt_, see: http://www.nltk.org/
- `Levenshtein`, see: https://pypi.python.org/pypi/python-Levenshtein/
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

    zcat tests/data/enwiki-20140102.tiny.xml.gz | ./wiki_edits.py

A bash script can be run to work with URL:

    ./run_with_dump_url.sh /path/to/work/dir /path/to/dir/for/edits http://wiki.dump.7z

For options see

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
