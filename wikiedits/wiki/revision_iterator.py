# -*- coding: utf-8 -*-

import re
from more_itertools import pairwise
from wikiedits.wiki import VANDALISM_REGEXES
from wikiedits.wiki.wiki_dump_parser import WikiDumpParser
from . import WikiExtractor

HTML_TAG_REGEX = r'<[^>]{1,20}?>'

cs=0
class RevisionIterator(object):

    def __init__(self, filename, lang='english'):
        self.dump = WikiDumpParser(filename)
        self.vandalism_regex = re.compile(VANDALISM_REGEXES[lang],
                                          re.IGNORECASE)

    def adjacent_revisios(self):
        prev_rev, rev = None, None

        for next_rev in self.dump.rev_iter():
            if next_rev is None:
                print("hallasd")
            global cs
            cs+=1
           # print(cs)
            comment = next_rev.get('comment', '')

            #
            # if self.vandalism_regex.search(comment) is not None:
            #     rev = None
            #     continue

            if prev_rev is not None and rev is not None:
                yield (prev_rev, rev)

            if rev is not None:
                prev_rev = rev

            next_rev['text'] = self.clean_markups(next_rev.get('text', ''))
            rev = next_rev

        if prev_rev is not None and rev is not None:
            yield (prev_rev, rev)



    def clean_revision(self,revision):
        text=revision.get('text','')
        clean_text = self.clean_markups(text)
        revision['text'] = clean_text
        return revision

    def adjacent_revisions(self):
        for old_rev, new_rev in pairwise(map(self.clean_revision,self.dump.rev_iter())):
            if self.vandalism_regex.search(new_rev.get('comment','')) is not None:
                continue
            yield old_rev, new_rev

    def clean_markups(self, text):

        clean_text = WikiExtractor.clean(text)
        clean_frags = WikiExtractor.compact(clean_text)
        clean_html = [re.sub(HTML_TAG_REGEX, '', frag)
                      for frag in clean_frags]

        return "\n".join(clean_html) if len(clean_html) > 0 else ""
