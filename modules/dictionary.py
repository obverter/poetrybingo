"""American English syllable counter using NLTK cmudict corpus."""

import sys, os
from string import punctuation
import json
import colors, corpus
import pprint
from corpus import load_corpus
import contextlib
from time import sleep

from nltk.corpus import cmudict

sys.path.append(os.path.join(sys.path[0], "poetrybingo", "utilities"))
sys.path.append(os.path.join(sys.path[0], "poetrybingo", "data"))
sys.path.append(os.path.join(sys.path[0], "poetrybingo", "modules"))


def CMU():
    return cmudict.dict()


from tqdm import tqdm


class DummyFile(object):
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)


@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = DummyFile(sys.stdout)
    yield
    sys.stdout = save_stdout


def missing_words():
    with open("../data/missing_words.json", "r") as f:
        return json.load(f)


corp = corpus.load_corpus()
word_set = missing_words()
cmu = cmudict.dict()
unique_words = set(corp.split(" "))


def cmudict_missing():
    """Find and return words in word set missing from cmudict."""
    exceptions = set()
    with tqdm(total=len(word_set), position=0) as pbar:
        for word in unique_words:
            if word.endswith("'s") or word.endswith("’s"):
                word = word[:-2]
    with tqdm(total=len(word_set), position=0, leave=True) as pbar:
        for count, word in tqdm(
            enumerate(unique_words, start=1), position=0, leave=True
        ):
            if word not in cmu | word_set:
                exceptions.add(word)
            pbar.update()

    print("\nexceptions:")
    print(exceptions)
    print("==================================================================")
    print(f"Unique words in corpus = {colors.GREEN(len(unique_words))}{colors.ENDC()}")

    print(
        f"Unique words I've already been taught = {colors.BLUE(len(word_set))}{colors.ENDC()}"
    )

    print(
        f"Unique words I need to be taught = {colors.WARNING(len(exceptions))}{colors.ENDC()}"
    )

    membership = (1 - len(exceptions) / len(cmu)) * 100
    coverage = (len(cmu) - len(exceptions)) / len(cmu) * 100
    missing = abs(len(word_set) - len(exceptions))
    print("==================================================================")
    print(
        f"\n{colors.GREEN('Haiku Roulette')}{colors.ENDC()} works best if the {colors.UNDERLINE('words words I need to be taught')}{colors.ENDC()} number is {colors.WARNING('0')}{colors.ENDC()}."
    )

    print(
        f"\nIf there are words I need to learn, maybe take a few minutes\nto add those words to the exceptions dictionary."
    )

    print(f"\nYou don't {colors.UNDERLINE('have')}{colors.ENDC()} to.")
    print(f"\nYou don't have to do anything, really.")
    print("\nBut the generated haiku will be slightly less horrible if you do.")
    return exceptions


def make_exceptions_dict(exceptions_set):
    """Return dictionary of words and syllable counts from set of words."""
    missing_words = {}
    print(
        "I'm going to show you each word that's missing from my syllable dictionary,\nand you're going to tell me the number of syllables in that word. You can edit things later on, so don't stress about mistakes. \n"
    )
    count = 1
    for word in exceptions_set:
        while True:
            print("- - -")
            print(f"This is word {count} of {len(exceptions_set)}.")
            num_sylls = input(f"How many syllables are in {word.upper()}: ")
            if num_sylls.isdigit():
                count += 1
                break
            else:
                print("Not a valid answer!", file=sys.stderr)
        missing_words[word] = int(num_sylls)
    print()
    pprint.pprint(missing_words, width=1)
    print("\nMake Changes to Dictionary Before Saving?")
    print(
        """
    0 - Exit & Save
    1 - Add a Word or Change a Syllable Count
    2 - Remove a Word
    """
    )

    while True:
        choice = input("\nEnter choice: ")
        if choice == "0":
            break
        elif choice == "1":
            word = input("\nWord to add or change: ")
            missing_words[word] = int(input(f"Enter number syllables in {word}: "))
        elif choice == "2":
            word = input("\nEnter word to delete: ")
            missing_words.pop(word, None)
    print("\nNew words or syllable changes:")
    pprint.pprint(missing_words, width=1)
    return missing_words


def save_exceptions(var):
    """Save exceptions dictionary as json file."""
    with open("../data/missing_words.json", "a+") as f:
        f.write(var)
    print("\nFile saved as missing_words.json")


def main():
    print(
        """

 _______   __    ______ .___________. __    ______   .__   __.      ___      .______     ____    ____
|       \ |  |  /      ||           ||  |  /  __  \  |  \ |  |     /   \     |   _  \    \   \  /   /
|  .--.  ||  | |  ,----'`---|  |----`|  | |  |  |  | |   \|  |    /  ^  \    |  |_)  |    \   \/   /
|  |  |  ||  | |  |         |  |     |  | |  |  |  | |  . `  |   /  /_\  \   |      /      \_    _/
|  '--'  ||  | |  `----.    |  |     |  | |  `--'  | |  |\   |  /  _____  \  |  |\  \----.   |  |
|_______/ |__|  \______|    |__|     |__|  \______/  |__| \__| /__/     \__\ | _| `._____|   |__|

Hang tight, I'm comparing your corpus to my syllable dictionary...
        """
    )

    missing_words()
    exceptions = cmudict_missing()
    miss = make_exceptions_dict(exceptions)
    save_exceptions(str(miss))
    return


if __name__ == "__main__":
    main()
