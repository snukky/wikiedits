#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# =============================================================================
#  Version: 2.6 (Oct 14, 2013)
#  Author: Giuseppe Attardi (attardi@di.unipi.it), University of Pisa
#	   Antonio Fuschetto (fuschett@di.unipi.it), University of Pisa
#
#  Contributors:
#	Leonardo Souza (lsouza@amtera.com.br)
#	Juan Manuel Caicedo (juan@cavorite.com)
#	Humberto Pereira (begini@gmail.com)
#	Siegfried-A. Gevatter (siegfried@gevatter.com)
#	Pedro Assis (pedroh2306@gmail.com)
#
# =============================================================================
#  Copyright (c) 2009. Giuseppe Attardi (attardi@di.unipi.it).
# =============================================================================
#  This file is part of Tanl.
#
#  Tanl is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License, version 3,
#  as published by the Free Software Foundation.
#
#  Tanl is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

"""Wikipedia Extractor:
Extracts and cleans text from Wikipedia database dump and stores output in a
number of files of similar size in a given directory.
Each file contains several documents in Tanl document format:
	<doc id="" url="" title="">
        ...
        </doc>

Usage:
  WikiExtractor.py [options]

Options:
  -c, --compress        : compress output files using bzip
  -b, --bytes= n[KM]    : put specified bytes per output file (default 500K)
  -B, --base= URL       : base URL for the Wikipedia pages
  -l, --link            : preserve links
  -n NS, --ns NS        : accepted namespaces (separated by commas)
  -o, --output= dir     : place output files in specified directory (default
                          current)
  -s, --sections	: preserve sections
  -h, --help            : display this help and exit
"""

import re
from html.entities import name2codepoint

### PARAMS ####################################################################

# This is obtained from the dump itself
prefix = None

##
# Whether to preseve links in output
#
keepLinks = False

##
# Whether to transform sections into HTML
#
keepSections = False

##
# Recognize only these namespaces
# w: Internal links to the Wikipedia
# wiktionary: Wiki dictionry
# wikt: shortcut for Wikctionry
#
acceptedNamespaces = {'w', 'wiktionary', 'wikt'}

##
# Drop these elements from article text
#
discardElements = {'gallery', 'timeline', 'noinclude', 'pre', 'table', 'tr', 'td', 'th', 'caption', 'form', 'input',
                   'select', 'option', 'textarea', 'ul', 'li', 'ol', 'dl', 'dt', 'dd', 'menu', 'dir', 'ref',
                   'references', 'img', 'imagemap', 'source'}

# =========================================================================
#
# MediaWiki Markup Grammar

# Template = "{{" [ "msg:" | "msgnw:" ] PageName { "|" [ ParameterName "=" AnyText | AnyText ] } "}}" ;
# Extension = "<" ? extension ? ">" AnyText "</" ? extension ? ">" ;
# NoWiki = "<nowiki />" | "<nowiki>" ( InlineText | BlockText ) "</nowiki>" ;
# Parameter = "{{{" ParameterName { Parameter } [ "|" { AnyText | Parameter } ] "}}}" ;
# Comment = "<!--" InlineText "-->" | "<!--" BlockText "//-->" ;
#
# ParameterName = ? uppercase, lowercase, numbers, no spaces, some special chars ? ;
#
# ===========================================================================

# Program version
version = '2.5'


##### Main function ###########################################################


def WikiDocument(out, id, title, text):
    url = get_url(id, prefix)
    header = '<doc id="%s" url="%s" title="%s">\n' % (id, url, title)
    # Separate header from text with a newline.
    header += title + '\n'
    header = header.encode('utf-8')
    text = clean(text)
    footer = "\n</doc>"
    out.reserve(len(header) + len(text) + len(footer))
    print(header, file=out)
    for line in compact(text):
        print(line.encode('utf-8'), file=out)
    print(footer, file=out)


def get_url(id, prefix):
    return "%s?curid=%s" % (prefix, id)


# ------------------------------------------------------------------------------


selfClosingTags = ['br', 'hr', 'nobr', 'ref', 'references']

# handle 'a' separetely, depending on keepLinks
ignoredTags = [
    'b', 'big', 'blockquote', 'center', 'cite', 'div', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'hiero', 'i', 'kbd', 'nowiki',
    'p', 'plaintext', 's', 'small', 'span', 'strike', 'strong',
    'sub', 'sup', 'tt', 'u', 'var',
]

placeholder_tags = {'math': 'formula', 'code': 'codice'}


##
# Normalize title


def normalizeTitle(title):
    # remove leading whitespace and underscores
    title = title.strip(' _')
    # replace sequences of whitespace and underscore chars with a single space
    title = re.compile(r'[\s_]+').sub(' ', title)

    m = re.compile(r'([^:]*):(\s*)(\S(?:.*))').match(title)
    if m:
        prefix = m.group(1)
        if m.group(2):
            optionalWhitespace = ' '
        else:
            optionalWhitespace = ''
        rest = m.group(3)

        ns = prefix.capitalize()
        if ns in acceptedNamespaces:
            # If the prefix designates a known namespace, then it might be
            # followed by optional whitespace that should be removed to get
            # the canonical page name
            # (e.g., "Category:  Births" should become "Category:Births").
            title = ns + ":" + rest.capitalize()
        else:
            # No namespace, just capitalize first letter.
            # If the part before the colon is not a known namespace, then we must
            # not remove the space after the colon (if any), e.g.,
            # "3001: The_Final_Odyssey" != "3001:The_Final_Odyssey".
            # However, to get the canonical page name we must contract multiple
            # spaces into one, because
            # "3001:   The_Final_Odyssey" != "3001: The_Final_Odyssey".
            title = prefix.capitalize() + ":" + optionalWhitespace + rest
    else:
        # no namespace, just capitalize first letter
        title = title.capitalize()
    return title


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.


def unescape(text):
    def fixup(m):
        text = m.group(0)
        code = m.group(1)
        try:
            if text[1] == "#":  # character reference
                if text[2] == "x":
                    return chr(int(code[1:], 16))
                else:
                    return chr(int(code))
            else:  # named entity
                return chr(name2codepoint[code])
        except:
            return text  # leave as is

    return re.sub(r"&#?(\w+);", fixup, text)


# Match HTML comments
comment = re.compile(r'<!--.*?-->', re.DOTALL)

# Match elements to ignore
discard_element_patterns = []
for tag in discardElements:
    pattern = re.compile(r'<\s*%s\b[^>]*>.*?<\s*/\s*%s>' % (tag, tag), re.DOTALL | re.IGNORECASE)
    discard_element_patterns.append(pattern)

# Match ignored tags
ignored_tag_patterns = []


def ignoreTag(tag):
    left = re.compile(r'<\s*%s\b[^>]*>' % tag, re.IGNORECASE)
    right = re.compile(r'<\s*/\s*%s>' % tag, re.IGNORECASE)
    ignored_tag_patterns.append((left, right))


for tag in ignoredTags:
    ignoreTag(tag)

# Match selfClosing HTML tags
selfClosing_tag_patterns = []
for tag in selfClosingTags:
    pattern = re.compile(r'<\s*%s\b[^/]*/\s*>' % tag, re.DOTALL | re.IGNORECASE)
    selfClosing_tag_patterns.append(pattern)

# Match HTML placeholder tags
placeholder_tag_patterns = []
for tag, repl in list(placeholder_tags.items()):
    pattern = re.compile(r'<\s*%s(\s*| [^>]+?)>.*?<\s*/\s*%s\s*>' % (tag, tag), re.DOTALL | re.IGNORECASE)
    placeholder_tag_patterns.append((pattern, repl))

# Match preformatted lines
preformatted = re.compile(r'^ .*?$', re.MULTILINE)

# Match external links (space separates second optional parameter)
externalLink = re.compile(r'\[\w+.*? (.*?)\]')
externalLinkNoAnchor = re.compile(r'\[\w+[&\]]*\]')

# Matches bold/italic
bold_italic = re.compile(r"'''''([^']*?)'''''")
bold = re.compile(r"'''(.*?)'''")
italic_quote = re.compile(r"''\"(.*?)\"''")
italic = re.compile(r"''([^']*)''")
quote_quote = re.compile(r'""(.*?)""')

# Matches space
spaces = re.compile(r' {2,}')

# Matches dots
dots = re.compile(r'\.{4,}')


# A matching function for nested expressions, e.g. namespaces and tables.


def dropNested(text, openDelim, closeDelim):
    openRE = re.compile(openDelim)
    closeRE = re.compile(closeDelim)
    # partition text in separate blocks { } { }
    matches = []  # pairs (s, e) for each partition
    nest = 0  # nesting level
    start = openRE.search(text, 0)
    if not start:
        return text
    end = closeRE.search(text, start.end())
    next = start
    while end:
        next = openRE.search(text, next.end())
        if not next:  # termination
            while nest:  # close all pending
                nest -= 1
                end0 = closeRE.search(text, end.end())
                if end0:
                    end = end0
                else:
                    break
            matches.append((start.start(), end.end()))
            break
        while end.end() < next.start():
            # { } {
            if nest:
                nest -= 1
                # try closing more
                last = end.end()
                end = closeRE.search(text, end.end())
                if not end:  # unbalanced
                    if matches:
                        span = (matches[0][0], last)
                    else:
                        span = (start.start(), last)
                    matches = [span]
                    break
            else:
                matches.append((start.start(), end.end()))
                # advance start, find next close
                start = next
                end = closeRE.search(text, next.end())
                break  # { }
        if next != start:
            # { { }
            nest += 1
    # collect text outside partitions
    res = ''
    start = 0
    for s, e in matches:
        res += text[start:s]
        start = e
    res += text[start:]
    return res


def dropSpans(matches, text):
    """Drop from text the blocks identified in matches"""
    matches.sort()
    res = ''
    start = 0
    for s, e in matches:
        res += text[start:s]
        start = e
    res += text[start:]
    return res


# Match interwiki links, | separates parameters.
# First parameter is displayed, also trailing concatenated text included
# in display, e.g. s for plural).
#
# Can be nested [[File:..|..[[..]]..|..]], [[Category:...]], etc.
# We first expand inner ones, than remove enclosing ones.
#
wikiLink = re.compile(r'\[\[([^[]*?)(?:\|([^[]*?))?\]\](\w*)')

parametrizedLink = re.compile(r'\[\[.*?\]\]')


# Function applied to wikiLinks


def make_anchor_tag(match):
    global keepLinks
    link = match.group(1)
    colon = link.find(':')
    if colon > 0 and link[:colon] not in acceptedNamespaces:
        return ''
    trail = match.group(3)
    anchor = match.group(2)
    if not anchor:
        anchor = link
    anchor += trail
    if keepLinks:
        return '<a href="%s">%s</a>' % (link, anchor)
    else:
        return anchor


def clean(text):
    # FIXME: templates should be expanded
    # Drop transclusions (template, parser functions)
    # See: http://www.mediawiki.org/wiki/Help:Templates
    text = dropNested(text, r'{{', r'}}')

    # Drop tables
    text = dropNested(text, r'{\|', r'\|}')

    # Expand links
    text = wikiLink.sub(make_anchor_tag, text)
    # Drop all remaining ones
    text = parametrizedLink.sub('', text)

    # Handle external links
    text = externalLink.sub(r'\1', text)
    text = externalLinkNoAnchor.sub('', text)

    # Handle bold/italic/quote
    text = bold_italic.sub(r'\1', text)
    text = bold.sub(r'\1', text)
    text = italic_quote.sub(r'&quot;\1&quot;', text)
    text = italic.sub(r'&quot;\1&quot;', text)
    text = quote_quote.sub(r'\1', text)
    text = text.replace("'''", '').replace("''", '&quot;')

    ################ Process HTML ###############

    # turn into HTML
    text = unescape(text)
    # do it again (&amp;nbsp;)
    text = unescape(text)

    # Collect spans

    matches = []
    # Drop HTML comments
    for m in comment.finditer(text):
        matches.append((m.start(), m.end()))

    # Drop self-closing tags
    for pattern in selfClosing_tag_patterns:
        for m in pattern.finditer(text):
            matches.append((m.start(), m.end()))

    # Drop ignored tags
    for left, right in ignored_tag_patterns:
        for m in left.finditer(text):
            matches.append((m.start(), m.end()))
        for m in right.finditer(text):
            matches.append((m.start(), m.end()))

    # Bulk remove all spans
    text = dropSpans(matches, text)

    # Cannot use dropSpan on these since they may be nested
    # Drop discarded elements
    for pattern in discard_element_patterns:
        text = pattern.sub('', text)

    # Expand placeholders
    for pattern, placeholder in placeholder_tag_patterns:
        index = 1
        for match in pattern.finditer(text):
            text = text.replace(match.group(), '%s_%d' % (placeholder, index))
            index += 1

    text = text.replace('<<', '«').replace('>>', '»')

    #############################################

    # Drop preformatted
    # This can't be done before since it may remove tags
    text = preformatted.sub('', text)

    # Cleanup text
    text = text.replace('\t', ' ')
    text = spaces.sub(' ', text)
    text = dots.sub('...', text)
    text = re.sub(r' (,:\.\)\]»)', r'\1', text)
    text = re.sub(r'(\[\(«) ', r'\1', text)
    text = re.sub(r'\n\W+?\n', '\n', text)  # lines with only punctuations
    text = text.replace(',,', ',').replace(',.', '.')
    return text


section = re.compile(r'(==+)\s*(.*?)\s*\1')


def compact(text):
    """Deal with headers, lists, empty sections, residuals of tables"""
    page = []  # list of paragraph
    headers = {}  # Headers for unfilled sections
    emptySection = False  # empty sections are discarded

    for line in text.split('\n'):

        if not line:
            continue
        # Handle section titles
        m = section.match(line)
        if m:
            title = m.group(2)
            lev = len(m.group(1))
            if keepSections:
                page.append("<h%d>%s</h%d>" % (lev, title, lev))
            if title and title[-1] not in '!?':
                title += '.'
            headers[lev] = title
            # drop previous headers
            for i in list(headers.keys()):
                if i > lev:
                    del headers[i]
            emptySection = True
            continue
        # Handle page title
        if line.startswith('++'):
            title = line[2:-2]
            if title:
                if title[-1] not in '!?':
                    title += '.'
                page.append(title)
        # handle lists
        elif line[0] in '*#:;':
            if keepSections:
                page.append("<li>%s</li>" % line[1:])
            else:
                continue
        # Drop residuals of lists
        elif line[0] in '{|' or line[-1] in '}':
            continue
        # Drop irrelevant lines
        elif (line[0] == '(' and line[-1] == ')') or line.strip('.-') == '':
            continue
        elif len(headers):
            items = list(headers.items())
            items.sort()
            for (i, v) in items:
                page.append(v)
            headers.clear()
            page.append(line)  # first line
            emptySection = False
        elif not emptySection:
            page.append(line)

    return page
