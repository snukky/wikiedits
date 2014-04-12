#!/usr/bin/python

import sys, os
import argparse
import logging

# it may be required if you have installed NLTK locally
#import nltk.data
# nltk.data.path.append('/home/user/.local/share/nltk_data')

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wiki_edits.edits_extractor import EditsExtractor


def main():
    args = parse_arguments()

    if args.debug: 
        set_log_level('debug')

    with open(args.old_text) as file:
        old_text = " ".join([line.rstrip() for line in file.readlines()])
    with open(args.new_text) as file:
        new_text = " ".join([line.rstrip() for line in file.readlines()])

    edits = EditsExtractor(lang=args.language,
                           min_words=args.min_words,
                           max_words=args.max_words,
                           length_diff=args.length_diff,
                           edit_ratio=args.edit_ratio)

    for old_edit, new_edit in edits.extract_edits(old_text, new_text):
        if not args.debug: 
            if args.tabify:
                print "%s\t%s" % (old_edit, new_edit)
            else:
                print old_edit
                print new_edit
                print ""

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extracts edited text fragments from two versions " \
                    "of the same text.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-o", "--old-text",
                        required=True,
                        help="file with older version of text")
    parser.add_argument("-n", "--new-text",
                        required=True,
                        help="file with newer version of text")
    parser.add_argument("-t", "--tabify",
                        action='store_true',
                        help="print output in OLD_EDIT-TAB-NEW_EDIT format")
    parser.add_argument("--debug", 
                        help="turn on debug mode",
                        action="store_true")

    group = parser.add_argument_group("selection options")
    group.add_argument("-l", "--language",
                       default="english",
                       help="specify language for NLTK sentence splitter")
    group.add_argument("--min-words",
                       type=int, default=2,
                       help="set minimum length of sentence in words")
    group.add_argument("--max-words",
                       type=int, default=120,
                       help="set maximum length of sentence in words")
    group.add_argument("--length-diff",
                       type=int, default=4,
                       help="set maximum difference in length between " \
                            "edited sentences")
    group.add_argument("--edit-ratio",
                       type=float, default=0.3,
                       help="set maximum relative difference in edit " \
                            "distance")

    return parser.parse_args()

def set_log_level(log_level):
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    main()
