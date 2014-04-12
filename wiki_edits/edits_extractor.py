from wiki_edits.diff_finder import DiffFinder
from wiki_edits.edits_selector import EditsSelector


class EditsExtractor:
    def __init__(self, **kwargs):
        self.diff = DiffFinder()
        self.selector = EditsSelector(**kwargs)
    
    def extract_edits(self, old_text, new_text):
        frags = self.diff.edited_fragments(old_text.split("\n"),
                                           new_text.split("\n"))
        edits = []
        for frag_pair in frags:
            for edit in self.selector.select_edits(*frag_pair):
                edits.append(edit)

        return edits
