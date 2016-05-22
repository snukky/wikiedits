#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import argparse

from joblib import Parallel, delayed


WIKIEDITS_DIR = os.path.abspath(os.path.dirname(__file__))
WIKIEDITS_OPTIONS = "-m -l polish"

JOBS = 4
PARALLEL_VERBOSE = False


def main():
    args = parse_user_args()

    debug("working dir: {}".format(args.work_dir))
    if not os.path.exists(args.work_dir):
        os.makedirs(args.work_dir)

    jobs = []

    with open(args.dump_files) as files:
        for idx, file in enumerate(files):

            jobs.append(delayed(process_dump_file) \
                (file.strip(), args.work_dir, args.extra_options))

    Parallel(n_jobs=args.jobs, verbose=PARALLEL_VERBOSE)(jobs)

def process_dump_file(file, work_dir, options):
    debug("processing dump: {}".format(file))

    file_base, file_ext = os.path.splitext(os.path.basename(file))
    edit_file = os.path.join(work_dir, file_base + '.edits')

    if os.path.exists(edit_file):
        debug("edit file exists: {}".format(edit_file))
        return True

    if file.startswith('http') or file.startswith('dumps.wikimedia.org'):
        download_file = os.path.join(work_dir, file_base + file_ext)

        if not os.path.exists(download_file):
            os.popen("wget -nc -O {} {}".format(download_file, file))
        else:
            debug("file already downloaded: {}".format(download_file))
        file = download_file

    cmd = ''

    if file_ext.startswith('.7z'):
        cmd = "7za e -so"
    elif file_ext.startswith('.xml'):
        cmd = "cat"
    elif file_ext.startswith('.gz'):
        cmd = "zcat"
    else:
        debug("file extension {} not recognized!".format(file_ext))
        return False

    os.popen("{cat} {dump} | python {dir}/wiki_edits.py {opts} > {edits}" \
        .format(cat=cmd, dir=WIKIEDITS_DIR, opts=options,
                dump=file, edits=edit_file))

    wc = os.popen("wc -l {}".format(edit_file)).read().strip().split()[0]
    debug("edit file collected with {} lines".format(wc))

    return True


def debug(msg):
    print >> sys.stderr, msg

def parse_user_args():
    parser = argparse.ArgumentParser(
        description="Collects edits from a list of Wikipedia dumps.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("dump_files", default="<STDIN>", nargs="?",
                        help="list of Wiki XML dump files or URLs")

    parser.add_argument("-w", "--work-dir", required=True,
                        help="directory for extracted edits")
    parser.add_argument("-e", "--extra-options", default=WIKIEDITS_OPTIONS,
                        help="extra options for script wiki_edits.py")
    parser.add_argument("-j", "--jobs", type=int, default=JOBS,
                        help="parallel jobs")

    args = parser.parse_args()
    if args.dump_files == "<STDIN>":
        args.dump_files = sys.stdin
    return args


if __name__ == "__main__":
    main()
