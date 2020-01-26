# -*- coding: utf-8 -*-

import re

from more_itertools import pairwise

from wikiedits.wiki import VANDALISM_REGEXES
from wikiedits.wiki.wiki_dump_parser import WikiDumpParser


class RevisionIterator:

    def __init__(self, filename, lang='english'):
        self.dump = WikiDumpParser(filename)
        self.vandalism_regex = VANDALISM_REGEXES[lang]

    def adjacent_revisions(self):
        dmp_itr = self.dump.rev_iter()
        for old_rev, new_rev in pairwise(dmp_itr):
            if new_rev.get('comment', '') is not None and self.vandalism_regex.search(
                    new_rev.get('comment', '')) is not None:
                continue
            yield old_rev, new_rev
