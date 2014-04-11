from wiki_edits.wiki.wiki_dump_parser import WikiDumpParser

import WikiExtractor
import re

class RevisionIterator:

    VANDALISM_REGEX = re.compile("vandal|stupid", re.IGNORECASE)
    
    def __init__(self, filename):
        self.dump = WikiDumpParser(filename)

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

        yield (prev_rev, rev)

    def clean_markups(self, text):
        if type(text) is not str:
            return ''
        
        clean_text = WikiExtractor.clean(text)
        clean_frags = WikiExtractor.compact(clean_text)

        return "\n".join(clean_frags) if len(clean_frags) > 0 else ""

    def __is_revert_vandalism(self, comment):
        if type(comment) is str:
            return bool(self.VANDALISM_REGEX.search(comment))
        return False
