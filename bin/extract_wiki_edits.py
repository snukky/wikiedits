#!/usr/bin/python

import sys, os
import argparse
import logging
import nltk.data

#nltk.data.path.append('/home/user/.local/share/nltk_data')
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from wiki_edits.wiki_edits_extractor import WikiEditsExtractor


def main():
    args = parse_arguments()

    if args.debug: 
        args.log_level = 'debug' 
    set_log_level(args.log_level)

    fi = args.dump_file or sys.stdin
    wiki = WikiEditsExtractor(fi)

    for edits, meta in wiki.extract_edits():
        if args.meta and edits:
            print "### %s" % meta
            print ""

        if not args.debug:
            for (old_edit, new_edit) in edits:
                print old_edit.encode('utf-8')
                print new_edit.encode('utf-8')
                print ""

def parse_arguments():
    help = "Extracts edited text fragments from Wikipedia revisions."

    parser = argparse.ArgumentParser(description=help)
    parser.add_argument("-f", "--dump-file",
                           help="specify XML dump file with all history " + 
                                "(read from STDIN by default")
    parser.add_argument("-m", "--meta", 
                        help="add revision meta data as id, user, comment etc.",
                        action="store_true")
    parser.add_argument("-l", "--log-level",
                        help="set log level")
    parser.add_argument("-d", "--debug", 
                        help="turn on debug mode",
                        action="store_true")

    return parser.parse_args()

def set_log_level(log_level):
    if log_level is not None:
        numeric_level = getattr(logging, log_level.upper(), None)
        logging.basicConfig(level=numeric_level)


if __name__ == "__main__":
    main()
