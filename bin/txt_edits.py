#!/usr/bin/python

import sys, os
import argparse
import logging
from tqdm import tqdm
# it may be required if you have installed NLTK locally
import nltk.data
nltk.data.path.append('$HOME/nltk_data')

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wikiedits.edit_extractor import EditExtractor
from wikiedits import LANGUAGES
batch_size = 10


def main():
    args = parse_user_args()

    if args.debug:
        set_logging_level('debug')

    old_text_file = open(args.old_text_file,'r')
    new_text_file = open(args.new_text_file,'r')
    old_text = old_text_file.readlines()
    new_text = new_text_file.readlines()

    for loopvar in tqdm(range(0,len(old_text),batch_size)):
        # Split into batches of sentences
        old_text_batch = " ".join(line.rstrip() for line in old_text[loopvar:loopvar+batch_size])
        new_text_batch = " ".join(line.rstrip() for line in new_text[loopvar:loopvar+batch_size])
        edits = EditExtractor(lang=args.language,
                              min_words=args.min_words,
                              max_words=args.max_words,
                              length_diff=args.length_diff,
                              edit_ratio=args.edit_ratio)
        if args.tabify:
            output = "{old}\t{new}"
            if args.scores:
                output += "\t{dist}\t{ratio}"
        else:
            output = "{old}\n{new}\n"
            if args.scores:
                output += "{dist} {ratio}\n"
        for old_edit, new_edit, scores in edits.extract_edits(old_text_batch, new_text_batch):
            print output.format(old=old_edit, new=new_edit,ratio=scores[0], dist=scores[1])
    old_text_file.close()
    new_text_file.close()


def set_loging_level(log_level):
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=numeric_level)


def parse_user_args():
    parser = argparse.ArgumentParser(
        description="Extracts edited text fragments from two versions " \
                    "of the same text.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("old_text_file", help="older version of text")
    parser.add_argument("new_text_file", help="newer version of text")

    parser.add_argument("-t", "--tabify", action='store_true',
                        help="print output in OLDEDIT-TAB-NEWEDIT format")
    parser.add_argument("-s", "--scores", action='store_true',
                        help="add levenshtein-based scores")
    parser.add_argument("--debug", action="store_true",
                        help="turn on debug mode")

    group = parser.add_argument_group("selection options")
    group.add_argument("-l", "--language", default="english",
                       help="specify language of NLTK sentence splitter",
                       choices=LANGUAGES)
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

    return parser.parse_args()



if __name__ == "__main__":
    main()
