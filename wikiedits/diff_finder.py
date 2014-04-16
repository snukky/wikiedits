import re
from difflib import ndiff, restore

class DiffFinder:

    def edited_fragments(self, old_frags, new_frags):
        try:
            raw_diff = ndiff(old_frags, new_frags)
        except:
            return []

        edits = []
        for edit in self.__diff_fragments(raw_diff):
            old_edit = '\n'.join(restore(edit, 1))
            new_edit = '\n'.join(restore(edit, 2))
            edits.append( (old_edit, new_edit) )
        return edits

    def edited_tokens(self, new_tokens, old_tokens):
        try:
            raw_diff = ndiff(new_tokens, old_tokens)
        except:
            return []

        edits = []
        for edit, start, end in self.__diff_tokens(raw_diff):
            old_edit = ' '.join(restore(edit, 1))
            new_edit = ' '.join(restore(edit, 2))
            edits.append( (old_edit, new_edit, start, end) )

        return edits
    
    def __diff_fragments(self, raw_diff):
        diffs = self.__clean_diff(raw_diff)
        actions = self.__diff_actions(diffs)

        positions = [(match.start(0), match.end(0))
                     for match in re.finditer(r'-+\++', actions)]

        return [diffs[start:end] for start, end in positions]

    def __diff_tokens(self, raw_diff):
        diffs = self.__clean_diff(raw_diff)
        actions = self.__diff_actions(diffs)

        results = []
        pos_shift = 0
        for start, end, mlen, plen in self.__edition_indexes(actions):
            start_pos = start - pos_shift
            end_pos = start_pos + mlen
            pos_shift += plen
            results.append( (diffs[start:end], start_pos, end_pos) )
        
        return results

    def __edition_indexes(self, actions):
        indexes = []         
        for match in re.finditer(r'(-+)?(\++)|(-+)(\++)?', actions):
            mlen = max(match.end(1) - match.start(1), 
                       match.end(3) - match.start(3))
            plen = max(match.end(2) - match.start(2),
                       match.end(4) - match.start(4))
            indexes.append( (match.start(0), match.end(0), mlen, plen) )

        return indexes

    def __clean_diff(self, diff):
        return [line for line in list(diff) if not line.startswith('?')]

    def __diff_actions(self, diffs):
        return ''.join([line[0] for line in diffs])
