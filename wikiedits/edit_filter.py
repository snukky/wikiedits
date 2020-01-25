# -*- coding: utf-8 -*-

import logging
import math

import Levenshtein
import nltk.data

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
            self.segmenter = nltk.data.load('tokenizers/punkt/%s.pickle' % lang)
        self.LEVENSHTEIN_RATIO_LOG_BASE = 20
        self.MIN_TEXT_LENGTH = min_chars  # in characters
        self.MIN_WORDS_IN_SENTENCE = min_words  # in words
        self.MAX_WORDS_IN_SENTENCE = max_words  # in words
        self.MAX_LENGTH_DIFF = length_diff  # on words
        self.MAX_LEVENSHTEIN_RATIO = edit_ratio  # on words
        self.LANG = lang

    def filter_edits(self, old_text, new_text):
        log.debug("processing texts:\n  >>> %s\n  >>> %s", old_text, new_text)
        if not self.__looks_like_text_edition(old_text, new_text):
            return []

        edits = []
        for old_sent, new_sent in self.__sentence_pairs(old_text, new_text):
            if self.LANG in IndicSentenceTokenizer.LANGUAGES:
                old_sent = old_sent.strip(IndicSentenceTokenizer.NON_INDIC)
                new_sent = new_sent.strip(IndicSentenceTokenizer.NON_INDIC)

            old_sent = old_sent.strip()
            new_sent = new_sent.strip()

            log.debug("processing sentences:\n  > %s\n  > %s",
                      old_sent, new_sent)

            scores = self.__looks_like_sentence_edition(old_sent, new_sent)
            if not scores:
                continue
            edits.append((old_sent, new_sent, scores))

        log.debug("got %i edited sentence(s)", len(edits))
        return edits

    def __looks_like_text_edition(self, old_text, new_text):
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

    def __looks_like_sentence_edition(self, old_sent, new_sent):
        if old_sent == new_sent:
            log.debug("sentences are equal")
            return False

        # the number of words in a sentence is obtained by counting the number
        # of spaces plus one
        counts = [old_sent.count(' ') + 1, new_sent.count(' ') + 1]
        diff = abs(counts[0] - counts[1])

        if diff > self.MAX_LENGTH_DIFF:
            log.debug("too large difference in number of words %i", diff)
            return False

        if min(counts) < self.MIN_WORDS_IN_SENTENCE:
            log.debug("shorter sentence has too few words")
            return False

        if max(counts) > self.MAX_WORDS_IN_SENTENCE:
            log.debug("longer sentence has too many words")
            return False

        ratio, dist = self.__levenshtein_ratio(old_sent, new_sent)

        if ratio > self.MAX_LEVENSHTEIN_RATIO:
            log.debug("too high levensthein ratio %.2f", ratio)
            return False

        return ratio, dist

    def __sentence_pairs(self, old_frag, new_frag):
        old_sents = self.__segmentize(old_frag)
        new_sents = self.__segmentize(new_frag)

        min_size = min(len(old_sents), len(new_sents))
        for idx in range(min_size):
            yield (' '.join(old_sents[idx].split()),
                   ' '.join(new_sents[idx].split()))

    def __segmentize(self, text):
        return [frag
                for sent in self.segmenter.tokenize(text)
                for frag in sent.split('; ')]

    def __levenshtein_ratio(self, old_sent, new_sent):
        old_words = old_sent.split()
        new_words = new_sent.split()

        min_words = min(len(old_words), len(new_words))
        dist = self.__levenshtein_on_words(old_words, new_words)
        ratio = dist / float(min_words) * math.log(min_words,
                                                   self.LEVENSHTEIN_RATIO_LOG_BASE)

        return ratio, dist

    def __levenshtein_on_words(self, words1, words2):
        char = 32  # 32 + 33 = 'A'
        word_map = {}
        for word in set(words1 + words2):
            word_map[word] = chr((char % 93) + 33)
            char += 1

        list1 = ''.join([word_map[word] for word in words1])
        list2 = ''.join([word_map[word] for word in words2])
        return Levenshtein.distance(list1, list2)
