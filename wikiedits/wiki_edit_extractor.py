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
        revs = enumerate(self.__revision_pair())
        while True:
            try:
                (index, (old_text, new_text, meta)) = next(revs)
                log.info(f"Processed Revisions: {index}")
                if new_text and old_text:
                    edits = self.extractor.extract_edits(old_text, new_text)
                    if edits:
                        n_edits += len(edits)
                        log.info(f"Processed Edits: {n_edits}")
                        yield edits, meta
            except StopIteration:
                log.info("Finished")
                break
            except (Exception, KeyboardInterrupt) as e:
                log.info(e)
                input()

    def __revision_pair(self):
        for old_rev, new_rev in self.revision.adjacent_revisions():
            meta = new_rev.copy()
            meta.pop('text')
            yield old_rev['text'], new_rev['text'], meta
