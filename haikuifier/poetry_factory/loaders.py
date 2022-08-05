import os, sys

sys.path.insert(0, "haikuifier/poetry_factory")

##### script imports ###########################################################
from nltk.corpus import cmudict
from poetry_factory import syllable_counter


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
    with open("../data/haiku_corpus.txt", "r") as f:
        return f.read()