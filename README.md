Wiki Edits 2.0
==============

A collection of scripts for automatic extraction of edited sentences from text
edition histories, such as Wikipedia revisions. It was used to create the WikEd
Error Corpus --- a corpus of corrective Wikipedia edits published in:

    @inproceedings{wiked2014,
        author = {Roman Grundkiewicz and Marcin Junczys-Dowmunt},
        title = {The WikEd Error Corpus: A Corpus of Corrective Wikipedia Edits and its Application to Grammatical Error Correction},
        booktitle = {Advances in Natural Language Processing -- Lecture Notes in Computer Science},
        editor = {Adam Przepiórkowski and Maciej Ogrodniczuk},
        publisher = {Springer},
        year = {2014},
        volume = {8686},
        pages = {478--490},
        url = {http://emjotde.github.io/publications/pdf/mjd.poltal2014.draft.pdf}
    }

WikEd Error Corpus
------------------

The corpus has been prepared for two languages:

* English: [wiked-v1.0.en.tgz](http://data.statmt.org/romang/wiked/wiked-v1.0.en.tgz), 4.2 GB
* English, cleaned & preprocessed: [wiked-v1.0.en.prepro.tgz](http://data.statmt.org/romang/wiked/wiked-v1.0.en.prepro.tgz), 2.0 GB
* Polish: [wiked-v1.0.pl.tgz](http://data.statmt.org/romang/wiked/wiked-v1.0.pl.tgz), 301 MB

The repository also includes format conversion scripts for WikEd. The scripts
work independently form Wiki Edits and can be found in the `bin` directory.

Requirements
------------

This is a new version of Wiki Edits and it is **not compatible** with the old
version! Back to commit 163d771 if you need old scripts.

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
already installed:

    sudo apt-get install python-pip
    sudo make all

Usage
-----

To extract edits from parallel texts:

    ./bin/txt_edits.py tests/data/lorem_ipsum.old.txt tests/data/lorem_ipsum.new.txt

And from a Wikipedia dump file:

    zcat tests/data/enwiki-20140102.tiny.xml.gz | ./bin/wiki_edits.py

The last script extracts edits from a list of dump files or URLs:

    ./bin/collect_wiki_edits.py -w /path/to/work/dir dumplist.txt

Language-specific options
-------------------------

All scripts are mostly language-independent. A few components need to be
updated to run the scripts for non-English languages:

- model for NLTK _punkt_ tokenizer,
  see: https://github.com/nltk/nltk_data/tree/gh-pages
- regular expressions for filtering reverted revisions in file:
  `wikiedits/wiki/__init__.py`
- list of supported languages in file: `wikiedits/__init__.py`

Currently supported languages: English, Polish, German.
