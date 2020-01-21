import unittest
from wikiedits.Indic_Sentence_Tokenizer import IndicSentenceTokenizer


class TestHindiSentenceTokenizer(unittest.TestCase):

    def setUp(self):

        self.tokenizer = IndicSentenceTokenizer()

    def test_tokenize_simple(self):
        text = """कालिंजर दुर्ग, दुर्ग है। बुन्देलखण्ड  धरोहर स्थल खजुराहो से ९७.७ किमी दूर है। इसे भारत के सजाता रहा है। इस दुर्ग में कई प्राचीन मन्दिर हैं। इनमें कई गुप्तकाल के हैं।  शिव ने यही तपस्या कर उसकी ज्वाला शांत की थी। """
        sent = ["कालिंजर दुर्ग, दुर्ग है।",
                "बुन्देलखण्ड  धरोहर स्थल खजुराहो से ९७.७ किमी दूर है।",
                "इसे भारत के सजाता रहा है।",
                "इस दुर्ग में कई प्राचीन मन्दिर हैं।",
                "इनमें कई गुप्तकाल के हैं।",
                "शिव ने यही तपस्या कर उसकी ज्वाला शांत की थी।"]
        self.assertListEqual(list(self.tokenizer.tokenize(text)), sent)

    def test_tokenize_empty(self):
        text = "   "
        sent = []
        self.assertListEqual(list(self.tokenizer.tokenize(text)), sent)

    def test_tokenize_other(self):
        text = "कालिंजर दुर्ग, भारतीय राज्य उत्तर प्रदेश के बांदा! विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर!? विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर!"
        sent = [
            "कालिंजर दुर्ग, भारतीय राज्य उत्तर प्रदेश के बांदा!",

            "विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर!?",
            "विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर!"
            ]
        self.assertListEqual(list(self.tokenizer.tokenize(text)), sent)

    def test_tokenize_space(self):
        text = "     विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर ! ? "
        sent = ["विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोहर ! ?"]
        self.assertListEqual(list(self.tokenizer.tokenize(text)), sent)

    def test_tokenize_noend(self):
        text = "विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोह"
        sent = ["विंध्य पर्वत पर स्थित यह दुर्ग विश्व धरोह"]
        self.assertListEqual(list(self.tokenizer.tokenize(text)), sent)
