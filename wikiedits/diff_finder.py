# -*- coding: utf-8 -*-

import re
from difflib import ndiff, restore


class DiffFinder(object):

    def edited_fragments(self, old_frags, new_frags):
        try:
            raw_diff = ndiff(old_frags, new_frags)
        except:
            return []

        edits = []
        for edit in self.__diff_fragments(raw_diff):
            old_edit = '\n'.join(restore(edit, 1))
            new_edit = '\n'.join(restore(edit, 2))
            edits.append((old_edit, new_edit))
        return edits

    def __diff_fragments(self, raw_diff):
        diffs = self.__clean_diff(raw_diff)
        actions = self.__diff_actions(diffs)

        positions = [(match.start(0), match.end(0))
                     for match in re.finditer(r'-+\++', actions)]

        return [diffs[start:end] for start, end in positions]

    def __clean_diff(self, diff):
        try:
            return [line for line in list(diff) if not line.startswith('?')]
        except:
            return []

    def __diff_actions(self, diffs):
        return ''.join([line[0] for line in diffs])
