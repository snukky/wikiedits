#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

SKIP_COMMENTS = True


def main():
    err = None
    edist = None
    ratio = None

    for line in sys.stdin:
        line = line.strip()

        if line.startswith('###'):
            m = re.match(r'### scores: {dist: (.*), ratio: (.*)}.*', line)
            if m:
                edist = m.group(1)
                ratio = m.group(2)
            if not SKIP_COMMENTS:
                print(line)
            err = None
        elif line:
            if err is None:
                err = line.replace('\t', '')
            else:
                cor = line.replace('\t', '')
                if edist and ratio:
                    print("{}\t{}\t{}\t{}".format(err, cor, edist, ratio))
                else:
                    print("{}\t{}".format(err, cor))
                err = None
                edist = None
                ratio = None


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: python {} < enwiki.xxx.edit > enwiki.xxx.txt"
              .format(sys.argv[0]))
        exit()
    main()
