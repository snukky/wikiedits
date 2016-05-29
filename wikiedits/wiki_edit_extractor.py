# -*- coding: utf-8 -*-

from wiki.revision_iterator import RevisionIterator
from wikiedits.edit_extractor import EditExtractor

class WikiEditExtractor(object):

    def __init__(self, filename, **kwargs):
        self.revision = RevisionIterator(filename, kwargs['lang'])
        self.extractor = EditExtractor(**kwargs)

    def extract_edits(self):
        for old_text, new_text, meta in self.__revision_pair():
            edits = self.extractor.extract_edits(old_text, new_text)
            if edits:
                yield (edits, meta)

    def __revision_pair(self):
        for old_rev, new_rev in self.revision.adjacent_revisions():
            if 'text' in old_rev and 'text' in new_rev:
                old_text = old_rev['text']
                new_text = new_rev['text']

                new_rev.pop('text', None)
                yield (old_text, new_text, new_rev)
