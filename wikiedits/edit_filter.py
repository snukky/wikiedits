# -*- coding: utf-8 -*-

import logging
import math

import Levenshtein

from .indic_sentence_tokenizer import IndicSentenceTokenizer

log = logging.getLogger(__name__)


class EditFilter:

    def __init__(self,
                 lang='english',
                 min_words=3,
                 max_words=120,
                 length_diff=4,
                 edit_ratio=0.3,
                 min_chars=10):

        if lang in IndicSentenceTokenizer.LANGUAGES:
            self.segmenter = IndicSentenceTokenizer()
        else:
            import nltk.data
            self.segmenter = nltk.data.load('tokenizers/punkt/%s.pickle' % lang)

        self.MIN_TEXT_LENGTH = min_chars  # in characters
        self.MIN_WORDS_IN_SENTENCE = min_words  # in words
        self.MAX_WORDS_IN_SENTENCE = max_words  # in words
        self.MAX_LENGTH_DIFF = length_diff  # on words
        self.MAX_LEVENSHTEIN_RATIO = edit_ratio  # on words
        self.LANG = lang

    def filter_edits(self, old_text, new_text):
        log.debug("processing texts:\n  >>> %s\n  >>> %s", old_text, new_text)

        if not self.looks_like_text_edition(old_text, new_text):
            return []

        edits = []
        for old_sent, new_sent in self.sentence_pairs(old_text, new_text):

            # First remove all non Indic Characters
            if self.LANG in IndicSentenceTokenizer.LANGUAGES:
                old_sent = old_sent.translate(IndicSentenceTokenizer.NON_INDIC)
                new_sent = new_sent.translate(IndicSentenceTokenizer.NON_INDIC)

            old_sent = old_sent.strip()
            new_sent = new_sent.strip()

            log.debug("processing sentences:\n  > %s\n  > %s",
                      old_sent, new_sent)

            scores = self.looks_like_sentence_edition(old_sent, new_sent)
            if not scores:
                continue

            edits.append((old_sent, new_sent, scores))

        return edits

    def looks_like_text_edition(self, old_text, new_text):
        if not old_text or not new_text:
            log.debug("either old or new text fragment is empty")
            return False
        if old_text == new_text:
            log.debug("texts are equal")
            return False

        if len(old_text) < self.MIN_TEXT_LENGTH \
                or len(new_text) < self.MIN_TEXT_LENGTH:
            log.debug("either old or new text fragment is too short")
            return False

        return True

    def looks_like_sentence_edition(self, old_sent, new_sent):
        if old_sent == new_sent:
            log.debug("sentences are equal")
            return False

        # the number of words in a sentence is obtained by counting the number
        # of spaces plus one
        counts = (old_sent.count(' ') + 1, new_sent.count(' ') + 1)
        diff = abs(counts[0] - counts[1])

        if diff > self.MAX_LENGTH_DIFF:
            #log.debug("too large difference in number of words %i", diff)
            return False

        if min(counts) < self.MIN_WORDS_IN_SENTENCE:
            #log.debug("shorter sentence has too few words")
            return False

        if max(counts) > self.MAX_WORDS_IN_SENTENCE:
            #log.debug("longer sentence has too many words")
            return False

        ratio, dist = self.levenshtein_ratio(old_sent, new_sent)

        if ratio > self.MAX_LEVENSHTEIN_RATIO:
            #log.debug("too high levensthein ratio %.2f", ratio)
            return False

        return ratio, dist

    def sentence_pairs(self, old_frag, new_frag):
        old_sents = self.segmentize(old_frag)
        new_sents = self.segmentize(new_frag)
        return zip(old_frag,new_frag)

    def segmentize(self, text):
        return [frag for sent in self.segmenter.tokenize(text)
                for frag in sent.split('; ')]

    def levenshtein_ratio(self, old_sent, new_sent):
        old_words = old_sent.split()
        new_words = new_sent.split()

        min_words = min(len(old_words), len(new_words))
        dist = self.levenshtein_on_words(old_words, new_words)
        ratio = dist / float(min_words) * math.log(min_words,
                                                   20)

        return ratio, dist

    def levenshtein_on_words(self, words1, words2):
        char = 32  # 32 + 33 = 'A'
        word_map = {}
        for word in set(words1 + words2):
            word_map[word] = chr((char % 93) + 33)
            char += 1

        list1 = ''.join([word_map[word] for word in words1])
        list2 = ''.join([word_map[word] for word in words2])
        return Levenshtein.distance(list1, list2)
