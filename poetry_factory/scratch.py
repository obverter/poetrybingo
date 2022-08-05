import json
from deepdiff import DeepDiff
from requests import head

import sys
from string import punctuation
import pprint
import json
import pandas as pd
from nltk.corpus import cmudict
import re
from loaders import whats_new

cmudict = cmudict.dict()  # CMU Pronouncing Dictionary


cmu = list(cmudict.keys())
def whats_new():
    try:
        with open("data/missing_words.json", "r") as f:
            current_exceptions_dict = json.load(f)
    except:
        with open("data/missing_words.json", "r") as f:
            current_exceptions_dict = json.load(f)

    current = list(current_exceptions_dict.keys())

    try:
        with open("headlines.json", "r") as f:
            headlines = json.load(f)
    except:
        with open("notebooks/headlines.json", "r") as f:
            headlines = json.load(f)
    headlines = list(headlines["headline"])

    def dump_current(missing_words):
        with open("data/missing_words.json", "w") as f:
            missing_words = json.dump(missing_words, f)
            missing_words = re.sub('[^0-9a-zA-Z]+', '', missing_words)
        return missing_words

    def load_text_file(file):
        """Return a text file as a string."""
        with open(file) as f:
            return f.read()

    test = dump_current(current_exceptions_dict)
    keys = list(test.keys())

    gold = keys + cmu

    lesson = load_text_file("data/haiku_corpus.txt")

    # NEW GETS ME THE DELTA I NEED TO UPDATE THE SYLLABLE DICT
    new = [word for word in lesson if word not in gold]
    return new


new = whats_new()
print(new)
