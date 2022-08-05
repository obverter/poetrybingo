import re
import json
from string import punctuation
from cachetools import cached
from nltk.corpus import cmudict

def cmudict(dict):



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


def whats_new():
    """
    It takes a text file, and returns a list of words that are not in the CMU dictionary

    :return: A list of words that are not in the syllable dictionary.
    """
    cmu = get_cmu()

    try:
        with open("missing_words.json", "r") as f:
            current_exceptions = json.load(f)
    except Exception:
        with open("../data/missing_words.json", "r") as f:
            current_exceptions = json.load(f)
    current = list(current_exceptions.keys())
    try:
        with open("headlines.json", "r") as f:
            headlines = json.load(f)
    except Exception:
        with open("../notebooks/headlines.json", "r") as f:
            headlines = json.load(f)
    headlines = list(headlines["headline"])

    def dump_current(missing_words):
        with open("missing_words.json", "w") as f:
            missing_words = json.dump(missing_words, f)
            missing = re.sub("[^0-9a-zA-Z]+", "", str(missing_words))
        return missing

    def load_text_file(file):
        """Return a text file as a string."""
        with open(file) as f:
            return f.read()

    test = dump_current(current_exceptions)
    # keys = list(test.keys())
    # keys = list(keys)
    gold = test + cmu
    lesson = load_text_file("haiku_corpus.txt")
    new = [word for word in lesson if word not in gold]
    return new


@cached(cache={})
def get_cmu():
    return str(cmudict.dict())


def get_haiku_corpus():
    with open("data/haiku_corpus.json", "r") as f:
        return json.load(f)

def dump_haiku(haiku_corpus):
    with open("../data/haiku_corpus.json", "w") as f:
        haiku_json = json.dump(haiku_corpus, f)
        haiku_json = re.sub("[^0-9a-zA-Z]+", "", str(haiku_json))
    return json.load(f)


def get_headlines():
    with open("headlines.json", "r") as f:
        return json.load(f)


headlines = get_headlines()


def get_trainer():
    """
    It takes the headlines from the dataframe, removes extra spaces, joins them
    together, and writes them to a text file
    """

    heads = headlines["headline"]
    heads = heads.str.replace("  ", "")
    heads = heads.to_list()
    lesson = lesson = " ".join(heads)
    lesson = lesson.replace(" ...", "").lower()
    lesson = lesson.replace("  ", " ")
    with open("../data/lesson.txt", "w") as f:
        f.write(lesson)


def get_current_exceptions():
    """
    It opens the file `data/missing_words.json` and reads the contents into a Python
    dictionary
    :return: A dictionary of words that are missing from the dictionary.
    """

    with open("missing_words.json", "r") as f:
        return json.load(f)


current_exceptions = get_current_exceptions()


def load_haiku(filename):
    """
    It opens a file, reads it, replaces all hyphens with spaces, and splits the
    resulting string into a set of words

    :param filename: the name of the file to open
    :return: A set of all the words in the haiku corpus.
    """

    with open(filename) as in_file:
        return set(in_file.read().replace("-", " ").split())


def cmudict_missing(word_set):
    """
    It compares the words in the corpus to the words in the cmudict, and returns a
    list of words that are in the corpus but not in the cmudict

    :param word_set: a set of all the words in the corpus
    :return: A set of words that are not in the cmudict.
    """

    exceptions = set()
    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if word not in cmudict:
            exceptions.add(word)
    print("\nexceptions:")
    print(*exceptions, sep="\n")
    print(
        f"{bcolors.OKCYAN}=================================================================={bcolors.ENDC}"
    )
    print(f"Unique words in corpus = {bcolors.OKGREEN}{len(word_set)}{bcolors.ENDC}")
    print(
        f"Unique words in corpus not in cmudict = {bcolors.WARNING}{len(exceptions)}{bcolors.ENDC}"
    )
    print(
        f"Number of words in current exceptions dictionary = {bcolors.OKCYAN}{len(current_exceptions)}{bcolors.ENDC}"
    )
    membership = (1 - len(exceptions) / len(word_set)) * 100
    coverage = (len(current_exceptions) / len(exceptions)) * 100
    missing = abs(len(current_exceptions) - len(exceptions))
    print("Corpus cmudict membership = {:.1f}{}".format(membership, "%"))
    print("Exceptions dict coverage = {:.1f}{}".format(coverage, "%"))
    print(
        f"Corpus words missing from both cmudict and exceptions = {bcolors.FAIL}{missing}{bcolors.ENDC}."
    )
    print(
        f"{bcolors.OKCYAN}=================================================================={bcolors.ENDC}"
    )
    print(
        f"\nThe {bcolors.OKBLUE}Haikuifier{bcolors.ENDC} works best if the {bcolors.UNDERLINE}'words missing from both'{bcolors.ENDC} number is {bcolors.FAIL}0{bcolors.ENDC}.\nI.e. the red value on the last line of the blue-framed results block."
    )
    print(
        f"\nIf you're seeing a nonzero number, maybe input {bcolors.OKCYAN}'Y'{bcolors.ENDC}\nand add some words to the exceptions dictionary."
    )
    print(f"\nYou don't {bcolors.UNDERLINE}have{bcolors.ENDC} to.")
    print(f"\nYou don't have to do anything, really.")
    print("\nBut the generated haiku will be slightly less horrible if you do.")
    print(f"{bcolors.UNDERLINE}                      {bcolors.ENDC}")

    return exceptions
