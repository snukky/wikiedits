import string


class IndicSentenceTokenizer:
    LANGUAGES = ('hindi', 'bengali', 'punjabi')
    NON_INDIC_CHAR = string.ascii_letters
    NON_INDIC = str.maketrans(NON_INDIC_CHAR, " " * len(NON_INDIC_CHAR))

    def tokenize(self, text):
        sentence_end = ('|', '।', '!', '?')
        pos = [0] * len(sentence_end)
        while len(text) > 0:
            for i in range(len(sentence_end)):
                pos[i] = text.find(sentence_end[i])
            if not pos.count(-1) == len(pos):
                splitting_point = min([x for x in pos if not x == -1])
                if text[splitting_point] == '!':
                    m = splitting_point
                    m = m + 1
                    while m < len(text):
                        if text[m] == ' ':
                            m = m + 1
                        elif text[m] == '?':
                            splitting_point = m
                            break
                        else:
                            break
                if splitting_point + 1 < len(text) and text[splitting_point] in '?!':
                    splitting_point += 1
                sentence = text[:splitting_point + 1]
                text = text[splitting_point + 1:]
                ans = sentence
            else:
                ans = text
                text = ""
            ans = ans.rstrip()
            ans = ans.lstrip()
            if len(ans) > 1:
                yield ans
