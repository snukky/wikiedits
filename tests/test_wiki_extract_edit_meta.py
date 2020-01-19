import gzip
import os
import unittest

from wikiedits.wiki_edit_extractor import WikiEditExtractor


class WikiEditExtractorTest(unittest.TestCase):
    WIKI_TEMP_FILE = "enwiki.temp.xml"

    def setUp(self):
        file_name = os.path.join(os.path.dirname(__file__),
                                 "data",
                                 "enwiki-20140102.tiny.xml.gz")

        dump = gzip.open(file_name, "r")
        with open(self.WIKI_TEMP_FILE, "wb") as file:
            file.write(dump.read())
        dump.close()

        self.wiki = WikiEditExtractor(self.WIKI_TEMP_FILE,
                                      lang='english',
                                      min_words=3,
                                      max_words=120,
                                      length_diff=4,
                                      edit_ratio=0.3,
                                      min_chars=10)

    def tearDown(self):
        os.remove(self.WIKI_TEMP_FILE)

    def test_wiki_extract_edit_meta(self):
        verified_meta_values = [{'comment': 'term in bold', 'timestamp': '2002-03-01T00:13:17Z', 'id': '42733',
                                 'contributor': {'ip': '213.253.39.175'}, 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'comment': '*', 'timestamp': '2002-04-02T09:53:06Z', 'id': '42740',
                                 'contributor': {'ip': '206.82.16.35'}, 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'comment': 'more about the individualist anarchists way of thinking',
                                 'timestamp': '2002-04-26T07:02:43Z', 'id': '61039',
                                 'contributor': {'ip': '80.65.225.191'}, 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'comment': 'adjusted reference to anomie.', 'timestamp': '2002-05-01T20:54:35Z',
                                 'id': '61193', 'contributor': {'username': 'Eclecticology', 'id': '372'},
                                 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'comment': '*', 'timestamp': '2002-05-01T21:24:53Z', 'id': '101951',
                                 'contributor': {'username': 'Eclecticology', 'id': '372'},
                                 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'contributor': {'username': 'DanKeshet', 'id': '170'},
                                 'timestamp': '2002-07-17T12:08:12Z', 'page': {'id': '12', 'title': 'Anarchism'},
                                 'id': '120190'},
                                {'comment': 'lang links: +fr, pl', 'timestamp': '2002-07-23T01:12:22Z', 'id': '122974',
                                 'contributor': {'username': 'Brion VIBBER', 'id': '51'},
                                 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'contributor': {'username': '15.22', 'id': '0'}, 'timestamp': '2002-07-24T19:50:04Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '122979'},
                                {'contributor': {'ip': '213.22.28.52'}, 'timestamp': '2002-07-25T09:12:57Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '133814'},
                                {'comment': 'corrected spelling for "assinated" to "assassinated"',
                                 'timestamp': '2002-08-01T10:07:46Z', 'id': '171554',
                                 'contributor': {'ip': '151.140.141.30'}, 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'contributor': {'username': 'Tzartzam', 'id': '3624'},
                                 'timestamp': '2002-08-24T09:57:26Z', 'page': {'id': '12', 'title': 'Anarchism'},
                                 'id': '178505'},
                                {'contributor': {'username': 'Quercusrobur', 'id': '3741'},
                                 'timestamp': '2002-09-02T11:42:36Z', 'page': {'id': '12', 'title': 'Anarchism'},
                                 'id': '193391'},
                                {'comment': 'changed general strike wikilink', 'timestamp': '2002-09-03T15:28:25Z',
                                 'id': '194121', 'contributor': {'username': 'Tzartzam', 'id': '3624'},
                                 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'contributor': {'username': 'Quercusrobur', 'id': '3741'},
                                 'timestamp': '2002-09-07T03:20:22Z', 'page': {'id': '12', 'title': 'Anarchism'},
                                 'id': '206270'},
                                {'comment': 'fixed link to politics', 'timestamp': '2002-09-19T15:15:21Z',
                                 'id': '304668', 'contributor': {'username': 'Chuck Smith', 'id': '38'},
                                 'page': {'id': '12', 'title': 'Anarchism'}},
                                {'contributor': {'ip': '195.149.37.19'}, 'timestamp': '2002-09-26T18:22:07Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '316677'},
                                {'contributor': {'username': 'Lir', 'id': '4369'}, 'timestamp': '2002-09-28T07:09:23Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '320147'},
                                {'contributor': {'username': 'Lir', 'id': '4369'}, 'timestamp': '2002-09-28T07:30:37Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '320173'},
                                {'contributor': {'username': 'Graft', 'id': '2886'},
                                 'timestamp': '2002-10-01T03:16:46Z', 'page': {'id': '12', 'title': 'Anarchism'},
                                 'id': '327396'},
                                {'contributor': {'username': 'Lir', 'id': '4369'}, 'timestamp': '2002-10-02T15:40:15Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '331307'},
                                {'contributor': {'username': 'Lir', 'id': '4369'}, 'timestamp': '2002-10-02T15:48:04Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '331331'},
                                {'contributor': {'username': 'Lir', 'id': '4369'}, 'timestamp': '2002-10-02T15:48:46Z',
                                 'page': {'id': '12', 'title': 'Anarchism'}, 'id': '331334'}]

        for edits, meta in self.wiki.extract_edits():
            verified_meta_value = verified_meta_values.pop(0)
            self.assertDictEqual(meta, verified_meta_value)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
