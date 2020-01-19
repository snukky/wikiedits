import gzip
import os
import unittest

from wikiedits.wiki.wiki_dump_parser import WikiDumpParser


class WikiDumpParserTest(unittest.TestCase):
    WIKI_TEMP_FILE = "enwiki.temp.xml"

    def setUp(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data",
                                 "enwiki-20140102.tiny.xml.gz")

        dump = gzip.open(file_name, "rb")
        with open(self.WIKI_TEMP_FILE, "wb") as file:
            file.write(dump.read())
        dump.close()

        self.parser = WikiDumpParser(self.WIKI_TEMP_FILE)

    def tearDown(self):
        os.remove(self.WIKI_TEMP_FILE)

    def test_rev_iter(self):
        rev = next(self.parser.rev_iter())

        self.assertTrue('id' in rev)
        self.assertTrue('contributor' in rev)
        self.assertTrue('page' in rev)
        self.assertTrue('timestamp' in rev)
        self.assertTrue('text' in rev)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
