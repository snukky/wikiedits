#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys


def main():
    for line in sys.stdin:
        if not line.startswith('###'):
            wdiff = line.strip().replace("\t", ' ')
            print(source_line(wdiff) + "\t" + target_line(wdiff))


def source_line(wdiff):
    return re.sub(r" *{\+.*?\+} *", ' ', re.sub(r" *\[-(.*?)-\] *", r" \1 ", wdiff)).strip()


def target_line(wdiff):
    return re.sub(r" *\[-.*?-\] *", ' ', re.sub(r" *{\+(.*?)\+} *", r" \1 ", wdiff)).strip()


if __name__ == '__main__':
    main()
