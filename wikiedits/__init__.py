#  -*- coding: utf-8 -*-
import re

LANGUAGES = [
    'english',
    'polish',
    'german',
    'hindi',
    'bengali',
    'punjabi'
]

INDIC_GRAMMAR_REGEX = re.compile("व्याक|वर्तनी|मात्रा|grammar|grammatical|grammer|पाठ|विराम|चिह्न|ব্যাকরণ|ਵਿਆਕਰਣ", re.IGNORECASE)

