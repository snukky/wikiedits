Wiki Edits
==========

A collection of scripts for automatic extraction of edited sentences
from text edition histories, such as Wikipedia revisions. It was used
to build the WikEd Error Corpus - a corpus of corrective Wikipedia
edits. 


Requirements
------------

Required python packages:

- `nltk` with NLTK data, see: http://www.nltk.org/
- `Levenshtein`, see: https://pypi.python.org/pypi/python-Levenshtein/

Run tests by typing `nosetests` from main directory:


Usage
-----

Example usage from `bin` directory:

    ./extract_edits.py -o ../tests/data/lorem_ipsum.old.txt -n ../tests/data/lorem_ipsum.new.txt

And with Wikipedia dump file:

    zcat ../tests/data/enwiki-20140102.tiny.xml.gz | ./extract_wiki_edits.py

A bash script can be run to work with URL:

    ./run_with_dump_url.sh /path/to/work/dir /path/to/dir/for/edits http://wiki.dump.7z


Language-specific options
-------------------------

All scripts are mostly language-independent. Only two components need to
be checked or updated to run these scripts for non-English language:

- an availability of a model for NLTK punkt tokenizer, 
  see: https://github.com/nltk/nltk_data/tree/gh-pages
- regular expressions for filtering out reverted revisions,
  see file: `wikiedits/wiki/revision_iterator.py`

Supported languages are: English, Polish.
