#  -*- coding: utf-8 -*-
import re

VANDALISM_REGEXES = {
    'english': "vandal|stupid|revert",
    'polish': "anulowan|wycofan|cofnię|cofnie|przywróc|przywroc|revert|rewert",
    'german': "revert|vandal|rückgängig",
    'hindi': "revert|पूर्ववत",
    'bengali': "revert|বাতিল",
    'punjabi': "revert|ਸੋਧਾਂ ਵਾਪਸ|ਨਕਾਰੀ"
}

VANDALISM_REGEXES = {language: re.compile(VANDALISM_REGEXES[language], re.IGNORECASE) for language in VANDALISM_REGEXES}