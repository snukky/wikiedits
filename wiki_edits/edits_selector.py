from wiki_edits.diff_finder import DiffFinder

import nltk.data
import Levenshtein
import math

import logging
logger = logging.getLogger(__name__)


class EditsSelector:

    def __init__(self, 
                 lang='english',
                 min_words=3,
                 max_words=120,
                 length_diff=4,
                 levenshtein_ratio=0.3):

        self.segmenter = nltk.data.load('tokenizers/punkt/%s.pickle' % lang)

        self.MIN_TEXT_LENGTH = 10                       # in characters
        self.MIN_WORDS_IN_SENTENCE = min_words          # in words
        self.MAX_WORDS_IN_SENTENCE = max_words          # in words
        self.MAX_LENGTH_DIFF = length_diff              # on words
        self.MAX_LEVENSHTEIN_RATIO = levenshtein_ratio  # on ascii words

    def select_edits(self, old_text, new_text):
        if not self.__looks_like_text_edition(old_text, new_text):
            return [] 

        edits = []
        for old_sent, new_sent in self.__sentence_pairs(old_text, new_text):
            logger.debug("processing sentences:\n  > %s\n  > %s", 
                         old_sent, new_sent)

            if self.__looks_like_sentence_edition(old_sent, new_sent):
                edits.append((old_sent, new_sent))
            else:
                continue
        
        logger.debug("got %i edited sentence(s)", len(edits))
        return edits    

    def __looks_like_text_edition(self, old_text, new_text):
        if old_text == new_text:
            logger.debug("texts are equal")
            return False

        if len(old_text) < self.MIN_TEXT_LENGTH \
                or len(new_text) < self.MIN_TEXT_LENGTH:
            logger.debug("either old or new text fragment is too short")
            return False
        
        return True

    def __looks_like_sentence_edition(self, old_sent, new_sent):
        if old_sent == new_sent:
            logger.debug("sentences are equal")
            return False
        
        # the number of words in a sentence is obtained by counting the number 
        # of spaces plus one
        counts = [old_sent.count(' ') + 1, new_sent.count(' ') + 1]
        diff = abs(counts[0] - counts[1])

        if diff > self.MAX_LENGTH_DIFF:
            logger.debug("too large difference in number of words %i", diff)
            return False

        if min(counts) < self.MIN_WORDS_IN_SENTENCE:
            logger.debug("shorter sentence has too few words")
            return False

        if max(counts) > self.MAX_WORDS_IN_SENTENCE:
            logger.debug("longer sentence has too many words")
            return False

        ratio = self.__levenshtein_ratio(old_sent, new_sent)

        if ratio > self.MAX_LEVENSHTEIN_RATIO:
            logger.debug("too high levensthein ratio %.2f", ratio)
            return False

        return True

    def __sentence_pairs(self, old_frag, new_frag):
        old_sents = self.__segmentize(old_frag)
        new_sents = self.__segmentize(new_frag)
        
        min_size = min(len(old_sents), len(new_sents))
        for idx in range(min_size):
            yield (old_sents[idx], new_sents[idx])

    def __segmentize(self, text):
        return [frag
                for sent in self.segmenter.tokenize(text)
                for frag in sent.split('; ')]
    
    def __levenshtein_ratio(self, old_sent, new_sent):
        old_words = old_sent.split()
        new_words = new_sent.split()

        min_words = min(len(old_words), len(new_words))
        dist = self.__levenshtein_on_words(old_words, new_words)

        return dist / float(min_words) * math.log(min_words, 20)

    def __levenshtein_on_words(self, words1, words2):
        char = 32   # 32 + 33 = 'A'
        word_map = {}
        for word in set(words1 + words2):
            word_map[word] = chr((char % 93) + 33)
            char += 1

        list1 = ''.join([word_map[word] for word in words1])
        list2 = ''.join([word_map[word] for word in words2])
        return Levenshtein.distance(list1, list2)
