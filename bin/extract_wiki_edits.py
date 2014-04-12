#!/usr/bin/python

import sys, os
import argparse
import logging

# it may be required if you have installed NLTK locally
#import nltk.data
#nltk.data.path.append('/home/user/.local/share/nltk_data')

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wiki_edits.wiki_edits_extractor import WikiEditsExtractor


def main():
    args = parse_arguments()

    if args.debug: 
        set_log_level('debug')

    wiki = WikiEditsExtractor(args.dump_file or sys.stdin, 
                              lang=args.language,
                              min_words=args.min_words,
                              max_words=args.max_words,
                              length_diff=args.length_diff,
                              edit_ratio=args.edit_ratio)

    for edits, meta in wiki.extract_edits():
        if args.meta_data and edits:
            print "### %s" % meta
            print ""

        if not args.debug:
            for (old_edit, new_edit) in edits:
                print old_edit.encode('utf-8')
                print new_edit.encode('utf-8')
                print ""

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extracts edited text fragments from Wikipedia revisions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--dump-file",
                        help="specify XML dump file with complete edit " \
                             "history")
    parser.add_argument("-m", "--meta-data", 
                        help="add revision meta data like comment, user etc.",
                        action="store_true")
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
