import unittest
import os
import gzip
from wikiedits.wiki.revision_iterator import RevisionIterator


class RevisionIteratorTest(unittest.TestCase):

    def setUp(self):
        dump_name = os.path.join(os.path.dirname(__file__),
                                 "data",
                                 "enwiki-20140102.tiny.xml.gz")
        self.dump = gzip.open(dump_name, "rb")
        self.rev = RevisionIterator(self.dump)

    def tearDown(self):
        self.dump.close()

    def test_adjacent_revisions(self):
        revisions = self.rev.adjacent_revisions()

        rev1, rev2 = next(revisions)
        self.assertTrue('text' in rev1)
        self.assertTrue('text' in rev2)

        rev3, rev4 = next(revisions)
        self.assertEqual(rev2['id'], rev3['id'])


def main():
    unittest.main()

if __name__ == '__main__':
    main()
