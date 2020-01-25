# -*- coding: utf-8 -*-

from wikiedits.diff_finder import DiffFinder
from wikiedits.edit_filter import EditFilter


import logging
log = logging.getLogger(__name__)


class EditExtractor:

    def __init__(self, **kwargs):
        self.diff = DiffFinder()
        self.filter = EditFilter(**kwargs)

    def extract_edits(self, old_text, new_text):
        frags = self.diff.edited_fragments(old_text.split("\n"),
                                           new_text.split("\n"))
        # Generator is not used as it doesn't allow to check how many edits
        # have been returned.
        try:
            return [edit for frag_pair in frags
                    for edit in self.filter.filter_edits(*frag_pair)]
        except:
            return []
