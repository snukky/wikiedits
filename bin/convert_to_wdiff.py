#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from difflib import SequenceMatcher

SKIP_COMMENTS = False
ONE_LINE_COMMENTS = False


def main():
    err = None
    cor = None
    comment = ''

    for line in sys.stdin:
        line = line.strip()

        if line.startswith('###'):
            if not SKIP_COMMENTS:
                comment += line + "\n"
            err = None
            cor = None
        elif line:
            if err is None:
                err = line
            else:
                cor = line

                if comment:
                    if ONE_LINE_COMMENTS:
                        print(minimize_comment(comment))
                    else:
                        print(comment.strip())
                    comment = ''

                text = wdiff(err.split(), cor.split())
                if text:
                    print(text)
                else:
                    print(cor)
                err = None
                cor = None

def minimize_comment(comment):
    return comment.replace("\n###   ", ' ').strip()
      #.replace("\n###", ',').replace('### ', '### {').strip() + '}'

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
        print("Example: cat enwiki.xxx.txt | perl path/to/mosesdecoder/.../tokenizer-for-wiked.perl -no-escape -skip | python convert_to_wdiff.py [--skip-comments] [--one-line-comments]")
        exit()

    if '--skip-comments' in sys.argv:
        SKIP_COMMENTS = True
    if '--one-line-comments' in sys.argv:
        ONE_LINE_COMMENTS = True
    main()
