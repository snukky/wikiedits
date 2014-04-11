import unittest
from wiki_edits.diff_finder import DiffFinder


class DiffFinderTest(unittest.TestCase):
    def setUp(self):
        self.diff = DiffFinder()

    def test_simple_edited_fragments(self):
        old_text = "a b c d e f G".split(' ')
        new_text = "a b b c D e f".split(' ')

        edits = self.diff.edited_fragments(old_text, new_text)
        
        self.assertEqual(1, len(edits))
        self.assertEqual(("d","D"), edits[0])

    def test_edited_fragments(self):
        old_text = "Ala ma kota.\nDawno, dawno temu.".split("\n")
        new_text = "Ala ma psa.\nDawno, dawno temu.\nI co z tego?".split("\n")

        edits = self.diff.edited_fragments(old_text, new_text)

        self.assertEqual(1, len(edits))
        self.assertEqual(("Ala ma kota.","Ala ma psa."), edits[0])

    def test_edited_tokens(self):
        old_tokens = "a b c d e f g".split(' ')
        new_tokens = "a b c D e f g".split(' ')

        edits = self.diff.edited_tokens(old_tokens, new_tokens)

        self.assertEqual(1, len(edits))
        self.assertEqual(("d","D"), edits[0][0:2])

        start_pos, end_pos = edits[0][2:4]

        self.assertEqual(3, start_pos)
        self.assertEqual(4, end_pos)
        self.assertEqual("d", old_tokens[start_pos:end_pos][0])
    
    def test_edited_tokens_on_complex_edition(self):
        old_tokens = "a b c d e f g".split(' ')
        new_tokens = "a c D e f g h".split(' ')

        edits = self.diff.edited_tokens(old_tokens, new_tokens)

        self.assertEqual(3, len(edits))
        self.assertEqual(("b","", 1, 2), edits[0])
        self.assertEqual(("d","D", 3, 4), edits[1])
        self.assertEqual(("","h", 7, 7), edits[2])

    def test_insert_first_token(self):
        old_tokens = "b c d e".split(' ')
        new_tokens = "a b c d e".split(' ')

        edits = self.diff.edited_tokens(old_tokens, new_tokens)

        self.assertEqual(1, len(edits))
        self.assertEqual(("","a", 0, 0), edits[0])
        

def main():
    unittest.main()

if __name__ == '__main__':
    main()
