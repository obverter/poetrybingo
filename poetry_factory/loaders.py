import os, sys
import json


##### script imports ###########################################################
from nltk.corpus import cmudict
import syllable_counter


##### assets ###################################################################

# Loading the cmudict file into a dictionary.
cmudict = cmudict.dict()


#####functions##################################################################


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def load_cmu():
    """
    Loads the CMU dictionary into a Python dictionary
    :return: A dictionary of words and their pronunciations.
    """
    return cmudict


def load_haiku():
    """
    It opens the file "haiku_corpus.txt" and returns the file object
    :return: A file object
    """
    try:
        with open('../data/haiku_corpus.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:

        with open("../../data/haiku_corpus.txt", "r") as f:
            return f.read()

def load_missing():
    try:
        with open('../data/missing_words.json') as f:
            missing_words = json.load(f)
    except Exception:
        with open('../../data/missing_words.json') as f:
            missing_words = json.load(f)
    return missing_words