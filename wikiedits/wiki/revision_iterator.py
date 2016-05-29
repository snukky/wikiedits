# -*- coding: utf-8 -*-

from wikiedits.wiki.wiki_dump_parser import WikiDumpParser
from wikiedits.wiki import VANDALISM_REGEXES

import WikiExtractor
import re

HTML_TAG_REGEX = r'<[^>]{1,20}?>'

class RevisionIterator(object):

    def __init__(self, filename, lang='english'):
        self.dump = WikiDumpParser(filename)
        self.vandalism_regex = re.compile(VANDALISM_REGEXES[lang],
                                          re.IGNORECASE)

    def adjacent_revisions(self):
        prev_rev, rev = None, None

        for next_rev in self.dump.rev_iter():
            comment = next_rev.get('comment', '')
            if self.__is_revert_vandalism(comment):
                rev = None
                continue

            if prev_rev is not None and rev is not None:
                yield (prev_rev, rev)

            if rev is not None:
                prev_rev = rev

            next_rev['text'] = self.clean_markups(next_rev.get('text', ''))
            rev = next_rev

        if prev_rev is not None and rev is not None:
            yield (prev_rev, rev)

    def clean_markups(self, text):
        if not text:
            return ""

        clean_text = WikiExtractor.clean(text)
        clean_frags = WikiExtractor.compact(clean_text)
        clean_html = [re.sub(HTML_TAG_REGEX, '', frag)
                      for frag in clean_frags]

        return "\n".join(clean_html) if len(clean_html) > 0 else ""

    def __is_revert_vandalism(self, comment):
        if type(comment) is str:
            return bool(self.vandalism_regex.search(comment))
        return False
