"""Find words in haiku corpus missing from cmudict & build exceptions dict."""
import sys, os
from string import punctuation
import pprint
import json
import pandas as pd
from nltk.corpus import cmudict
import dictionary, corpus

sys.path.insert(0, "poetrybingo/data")



def count_syllables(words):
    """Use corpora to count syllables in English word or phrase."""
    missing_words = dictionary.missing_words()

    words = words.replace('-', ' ')
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s")or word.endswith("’s"):
            word = word[:-2]
        if word in missing_words:
            num_sylls += missing_words[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1
    return num_sylls

def main():
    # imports
    missing_words = dictionary.get_missing_dict()
    build_dict = input("\nManually build an exceptions dictionary (y/n)? \n")
    if build_dict.lower() == "n":
        sys.exit()
    else:
        missing_words_dict = dictionary.make_exceptions_dict(missing_words)
        dictionary.save_exceptions(missing_words_dict)

if __name__ == '__main__':
    main()
