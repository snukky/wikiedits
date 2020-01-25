#  -*- coding: utf-8 -*-
import re

LANGUAGES = [
    'english',
    'polish',
    'german',
    'hindi',
    'bengali'
]

INDIC_GRAMMAR_REGEX = re.compile("व्याक|वर्तनी|मात्रा|grammar|grammatical|grammer|fixed|पाठ|विराम|चिह्न", re.IGNORECASE)
