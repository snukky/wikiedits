from wikiedits.diff_finder import DiffFinder
from wikiedits.edit_filter import EditFilter


class EditExtractor(object):

    def __init__(self, **kwargs):
        self.diff = DiffFinder()
        self.filter = EditFilter(**kwargs)
    
    def extract_edits(self, old_text, new_text):
        frags = self.diff.edited_fragments(old_text.split("\n"),
                                           new_text.split("\n"))

        # Generator is not used because it allows to check if how many edits
        # have been returned.
        edits = []
        for frag_pair in frags:
            for edit in self.filter.filter_edits(*frag_pair):
                edits.append(edit)
        return edits
