#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from difflib import SequenceMatcher

SKIP_COMMENTS = False
ONE_LINE_COMMENTS = False


def main():
    for line in sys.stdin:
        if line.startswith('### '):
            continue
        err, cor = line.strip().split("\t")[:2]

        text = wdiff(err.split(), cor.split())
        if text:
            print(text)
        else:
            print(cor)


def wdiff(err_toks, cor_toks):
    result = ''
    matcher = SequenceMatcher(None, err_toks, cor_toks)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        err = ' '.join(err_toks[i1:i2])
        cor = ' '.join(cor_toks[j1:j2])

        if tag == 'replace':
            result += "[-{}-] {{+{}+}} ".format(err, cor)
        elif tag == 'insert':
            result += "{{+{}+}} ".format(cor)
        elif tag == 'delete':
            result += "[-{}-] ".format(err)
        else:
            result += err + ' '

    return result.strip()


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Example: cat enwiki.xxx.tsv | python {}".format(sys.argv[0]))
        exit()
    main()
