#!/usr/bin/python

import sys, os
import argparse
import logging

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wiki_edits.edits_extractor import EditsExtractor


def main():
    args = parse_arguments()
    set_log_level(args.log_level)

    with open(args.old_text) as file:
        old_text = " ".join([line.rstrip() for line in file.readlines()])

    with open(args.new_text) as file:
        new_text = " ".join([line.rstrip() for line in file.readlines()])

    extractor = EditsExtractor()
    for old_edit, new_edit in extractor.extract_edits(old_text, new_text):
        if args.tabify:
            print "%s\t%s" % (old_edit, new_edit)
        else:
            print old_edit
            print new_edit
            print ""

def parse_arguments():
    help = "Extracts edited text fragments from two versions of the same text."

    parser = argparse.ArgumentParser(description=help)
    parser.add_argument("-o", "--old-text",
                        required=True,
                        help="file with older version of text")
    parser.add_argument("-n", "--new-text",
                        required=True,
                        help="file with newer version of text")
    parser.add_argument("-t", "--tabify",
                        action='store_true',
                        help="print output in OLD EDIT-TAB-NEW EDIT foramt")
    parser.add_argument("-l", "--log-level",
                        help="set log level")
    return parser.parse_args()

def set_log_level(log_level):
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    main()
