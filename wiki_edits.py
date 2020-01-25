#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import subprocess
import sys
from subprocess import PIPE
from urllib.parse import urlparse

import yaml

from wikiedits import LANGUAGES, INDIC_GRAMMAR_REGEX
from wikiedits.wiki_edit_extractor import WikiEditExtractor

log = logging.getLogger(__name__)

output_types = ("annotated", "unannotated")


def parse_user_args():
    parser = argparse.ArgumentParser(
        description="Extracts edited text fragments from Wikipedia revisions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input", default=sys.stdin, nargs="?",
                        help="Wiki XML dump with complete edit history")

    parser.add_argument("-m", "--meta-data", action="store_true",
                        help="add revision meta data like comment, user, etc.")
    parser.add_argument("-t", "--tabify", action='store_true',
                        help="print output in OLD_EDIT-TAB-NEW_EDIT format")
    parser.add_argument("-s", "--scores", action='store_true',
                        help="add levenshtein-based scores; require --tabify")
    parser.add_argument("--debug", action="store_true",
                        help="turn on debug mode")

    group = parser.add_argument_group("selection options")
    group.add_argument("-l", "--language", default="english",
                       help="specify language of NLTK sentence splitter",
                       choices=LANGUAGES)
    group.add_argument("--min-chars", type=int, default=10,
                       help="set` the minimum number of characters in a "
                            "sentence")
    group.add_argument("--min-words", type=int, default=2,
                       help="set minimum length of sentence in words")
    group.add_argument("--max-words", type=int, default=120,
                       help="set maximum length of sentence in words")
    group.add_argument("--length-diff", type=int, default=4,
                       help="set maximum difference in length between "
                            "edited sentences")
    group.add_argument("--edit-ratio", type=float, default=0.3,
                       help="set maximum relative difference in edit "
                            "distance")
    return parser.parse_args()


def main():
    args = parse_user_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    input_file, file_name = get_input_file(args.input)

    output = os.path.splitext(file_name)[0]
    out_files = {output_type: open(output + '.' + output_type + ".edits", 'w') for output_type in output_types}

    # Metadata Formatting Related Option
    if args.tabify:
        output_format = "{old}\t{new}\n"
        if args.scores:
            output_format += "\t{dist}\t{ratio}\n"
    else:
        output_format = "{old}\n{new}\n\n"
        if args.scores:
            output_format = "### scores: {{dist: {dist}, ratio: {ratio}}}\n" \
                            + output_format

    wiki = WikiEditExtractor(input_file,
                             lang=args.language,
                             min_words=args.min_words,
                             max_words=args.max_words,
                             length_diff=args.length_diff,
                             edit_ratio=args.edit_ratio,
                             min_chars=args.min_chars)

    for edits, meta in wiki.extract_edits():
        out = out_files[select_output(meta)]

        if args.meta_data and edits:
            out.write(format_meta_data(meta) + "\n")
        for x in edits:
            (old_edit, new_edit, scores) = x
            out.write(output_format.format(old=old_edit,
                                           new=new_edit,
                                           ratio=scores[0],
                                           dist=scores[1]))

    for out_file in out_files.values():
        out_file.close()


def download_file(input_name):
    file_name = os.path.basename(urlparse(input_name).path)
    if os.path.exists(file_name):
        log.info("edit file exists: {} for {}".format(file_name, input_name))
    else:
        log.info("downloading dump: {}".format(input_name))
        subprocess.run("wget -nc -O {} {}".format(file_name, input_name).split())
    return file_name


def get_input_file(input_name):
    log.info("processing dump: {}".format(input_name))

    # check if input is a url or a filename
    if input_name.startswith('http') or input_name.startswith('dumps.wikimedia.org'):
        file_name = download_file(input_name)
    else:
        file_name = input_name

    log.info("processing dump file: {}".format(file_name))
    file_base, file_ext = os.path.splitext(file_name)

    if file_ext.startswith('.7z'):
        process = subprocess.Popen(f"7za e -so {file_name}".split(), stdout=PIPE)
        input_file = process.stdout
    elif file_ext.startswith('.gz'):
        process = subprocess.Popen(f"zcat {file_name}".split(), stdout=PIPE)
        input_file = process.stdout
    elif file_ext.startswith('.xml'):
        input_file = open(input_name, 'rb')
    else:
        raise TypeError("file extension {} not recognized!".format(file_ext))

    return input_file, file_base


def format_meta_data(meta):
    lines = ["### %s" % line
             for line in yaml.dump(meta, allow_unicode=True).split('\n')
             if line]
    return '\n'.join(lines)


def select_output(meta):
    if 'comment' in meta and re.search(INDIC_GRAMMAR_REGEX,
                                       meta["comment"],re.IGNORECASE) is not None:
        output_type = 'annotated'
    else:
        output_type = 'unannotated'
    return output_type


if __name__ == "__main__":
    main()
