import unittest

from wikiedits.diff_finder import DiffFinder


class DiffFinderTest(unittest.TestCase):
    def setUp(self):
        self.diff = DiffFinder()

    def test_simple_edited_fragments(self):
        old_text = "a b c d e f G".split(' ')
        new_text = "a b b c D e f".split(' ')

        edits = self.diff.edited_fragments(old_text, new_text)

        self.assertEqual(1, len(edits))
        self.assertEqual(("d", "D"), edits[0])

    def test_edited_fragments(self):
        old_text = "Ala ma kota.\nDawno, dawno temu.".split("\n")
        new_text = "Ala ma psa.\nDawno, dawno temu.\nI co z tego?".split("\n")

        edits = self.diff.edited_fragments(old_text, new_text)

        self.assertEqual(1, len(edits))
        self.assertEqual(("Ala ma kota.", "Ala ma psa."), edits[0])


def main():
    unittest.main()


if __name__ == '__main__':
    main()
