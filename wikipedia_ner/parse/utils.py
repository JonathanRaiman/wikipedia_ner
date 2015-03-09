import xml_cleaner.wiki_markup_processing as wiki_processing
double_bracket_no_other_ref = wiki_processing.re.compile("\[\[([^\|\]]+)\]\]")

def get_article_links(sentence):
    """
    Uses regular expressions to extract
    links from text by looking for double brackets
    and optionally pipe characters to symbolic
    target and anchor text in wiki markup syntax

    Inputs
    ------

    sentence str: text to parse

    Output
    ------

    list<tuple<str, str>> : list of tuples of target and anchor texts

    """
    pairs_of_anchor_tags = [(target.strip(), anchor.strip()) for target, anchor in wiki_processing.anchortag_internal_link.findall(sentence)]
    other_links = [(match.strip(), match.strip()) for match in double_bracket_no_other_ref.findall(sentence)]
    return pairs_of_anchor_tags + other_links

import re
letters = re.compile("$[^a-zA-Z0-9]+")

def test_okay_sentence(s):
    return (\
        ".jpg" not in s           and \
        s.count("Category") < 2   and \
        "http" not in s           and \
        "ISBN" not in s           and \
        "File : | thumb" not in s and \
        ".htm" not in s           and \
        ".png" not in s)

def line_converter(lines, article_name):
    """
    Creates generator that takes the valid text from wiki xml dumps 
    and uses regular expressions to select only the lines
    in the wiki that uses intra wiki links and returns the triplets
    of valid tokenized sentence, article name, and tuples of targets
    and anchor text from intra wiki links.

    Inputs
    ------

    lines str: a block of text from a wiki
    article_name str: the name of the current article


    Outputs
    -------

    tuple<str, str, list<tuple<str, str>>> : triplets
    of valid tokenized sentence, article name, and tuples of targets
    and anchor text from intra wiki links.

    """
    for sentence in wiki_processing.to_raw_text_pairings(lines):
        sentence_cleaned = sentence
        sentence = " ".join(sentence).strip()
        if test_okay_sentence(sentence):
            sentence.replace("&lt;",  " < ").replace("&lt ;", " < ").replace("&gt;",  " > ").replace("&gt ;", " > ")
            links = get_article_links(sentence)
            if len(links) > 0:
                yield((wiki_processing.remove_brackets(sentence).split(" "), article_name, links))