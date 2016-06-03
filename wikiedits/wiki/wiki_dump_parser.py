# -*- coding: utf-8 -*-

from lxml import etree
import sys

class WikiDumpParser(object):

    def __init__(self, filename):
        self.context = etree.iterparse(filename)
        self.important_tags = ['id', 'timestamp', 'comment', 'text', 'title']

    def page_iter(self):
        pass

    def rev_iter(self):
        revision, page, contributor = {}, {}, {}

        for elem in self.__fast_iter():
            tag = self.__extract_tag(elem)

            if tag == 'id':
                if not revision: # page id
                    page['id'] = elem.text
                if tag not in revision: # revision id
                    revision['id'] = elem.text
                else: # user id
                    contributor['id'] = elem.text

            elif tag in ['username', 'ip']:
                contributor[tag] = elem.text

            elif tag == 'contributor':
                revision['contributor'] = contributor

            elif tag == 'revision':
                revision['page'] = page
                yield revision
                revision = {}
                contributor = {}

            elif tag == 'title':
                page['title'] = elem.text

            elif tag == 'page':
                page = {}
                revision = {}
                contributor = {}

            elif tag in self.important_tags:
                revision[tag] = elem.text

    def __fast_iter(self):
        """
        High-performance XML parsing with lxml, see:
        http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
        """
        try:
            for event, elem in self.context:
                if event == 'end':
                    yield elem

                elem.clear()
                while elem.getprevious() is not None:
                    del elem.getparent()[0]
        except etree.LxmlError as ex:
            print >>sys.stderr, "Iteration stopped due to lxml exception: {}" \
                .format(ex)
        finally:
            del self.context

    def __extract_tag(self, elem):
        return elem.tag.rsplit('}', 1)[-1]
