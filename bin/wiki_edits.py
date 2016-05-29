#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import logging
import yaml

# it may be required if you have installed NLTK locally
#import nltk.data
#nltk.data.path.append('$HOME/nltk_data')

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wikiedits.wiki_edit_extractor import WikiEditExtractor
from wikiedits import LANGUAGES


def main():
    args = parse_user_args()

    if args.debug:
        set_logging_level('debug')

    wiki = WikiEditExtractor(args.dump_file or sys.stdin,
                             lang=args.language,
                             min_words=args.min_words,
                             max_words=args.max_words,
                             length_diff=args.length_diff,
                             edit_ratio=args.edit_ratio,
                             min_chars=args.min_chars)

    output = "{}\t{}" if args.tabify else "{}\n{}\n"

    for edits, meta in wiki.extract_edits():
        if args.meta_data and edits:
            print format_meta_data(meta)

        for (old_edit, new_edit) in edits:
            print output.format(old_edit.encode('utf-8'),
                                new_edit.encode('utf-8'))

def format_meta_data(data):
    lines = ["### %s" % line
             for line in yaml.dump(data, allow_unicode=True).split('\n')
             if line]
    return '\n'.join(lines)

def parse_user_args():
    parser = argparse.ArgumentParser(
        description="Extracts edited text fragments from Wikipedia revisions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dump_file", default="<STDIN>", nargs="?",
                        help="Wiki XML dump with complete edit history")

    parser.add_argument("-m", "--meta-data", action="store_true",
                        help="add revision meta data like comment, user, etc.")
    parser.add_argument("-t", "--tabify", action='store_true',
                        help="print output in OLD_EDIT-TAB-NEW_EDIT format")
    # parser.add_argument("-s", "--scores", action='store_true',
                        # help="add scores; require --tabify")
    parser.add_argument("--debug", action="store_true",
                        help="turn on debug mode")

    group = parser.add_argument_group("selection options")
    group.add_argument("-l", "--language", default="english",
                       help="specify language of NLTK sentence splitter",
                       choices=LANGUAGES)
    group.add_argument("--min-chars", type=int, default=10,
                       help="set the minimum number of characters in a " \
                            "sentence")
    group.add_argument("--min-words", type=int, default=2,
                       help="set minimum length of sentence in words")
    group.add_argument("--max-words", type=int, default=120,
                       help="set maximum length of sentence in words")
    group.add_argument("--length-diff", type=int, default=4,
                       help="set maximum difference in length between " \
                            "edited sentences")
    group.add_argument("--edit-ratio", type=float, default=0.3,
                       help="set maximum relative difference in edit " \
                            "distance")

    args = parser.parse_args()
    if args.dump_file == "<STDIN>":
        args.dump_file = sys.stdin
    return args

def set_logging_level(log_level):
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    main()
