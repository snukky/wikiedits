# -*- coding: utf-8 -*-

import logging

from wikiedits.edit_extractor import EditExtractor
from .wiki.revision_iterator import RevisionIterator

log = logging.getLogger(__name__)


class WikiEditExtractor:

    def __init__(self, filename, **kwargs):
        self.revision = RevisionIterator(filename, kwargs['lang'])
        self.extractor = EditExtractor(**kwargs)

    def extract_edits(self):
        n_edits = 0
        for index, (old_text, new_text, meta) in enumerate(self.__revision_pair()):
            log.info(f"Processed Revisions: {index}")
            edits = self.extractor.extract_edits(old_text, new_text)
            if edits:
                n_edits += len(edits)
                log.info(f"Processed Edits: {n_edits}")
                yield (edits, meta)

    def __revision_pair(self):
        for old_rev, new_rev in self.revision.adjacent_revisions():
            if 'text' in old_rev and 'text' in new_rev:
                old_text = old_rev['text']
                new_text = new_rev['text']

                new_rev.pop('text', None)
                yield (old_text, new_text, new_rev)
