"""American English syllable counter using NLTK cmudict corpus."""

import sys
from string import punctuation
import json
import colors, corpus
import pprint
from corpus import load_corpus

from nltk.corpus import cmudict

sys.path.insert(0, "tmz-poetry/poetrybingo")
sys.path.insert(1, "poetrybingo/data")
sys.path.insert(3, "poetrybingo/data/corpus.txt")


def CMU():
    return cmudict.dict()


def missing_words():
    with open("../data/missing_words.json", "r") as f:
        return json.load(f)


corp = corpus.load_corpus()
word_set = missing_words()
cmu = CMU()
unique_words = set(corp.split(" "))


def cmudict_missing():
    """Find and return words in word set missing from cmudict."""
    exceptions = set()
    for word in corp.split():
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if word not in cmu:
            exceptions.add(word)
    print("\nexceptions:")
    print(exceptions)
    print("==================================================================")
    print(f"Unique words in corpus = {colors.GREEN(len(unique_words))}{colors.ENDC()}")
    print(
        f"Unique words in corpus not in cmudict = {colors.WARNING(len(exceptions))}{colors.ENDC()}"
    )
    print(
        f"Number of words in current exceptions dictionary = {colors.BLUE(len(word_set))}{colors.ENDC()}"
    )
    membership = (1 - len(exceptions) / len(cmu)) * 100
    coverage = ((len(cmu) - len(exceptions)) / len(cmu)) * 100
    missing = abs(len(word_set) - len(exceptions))
    print(
        f"Corpus words missing from both cmudict and exceptions = {colors.FAIL(missing)}{colors.ENDC()}."
    )
    print("==================================================================")
    print(
        f"\n{colors.GREEN('Haiku Roulette')}{colors.ENDC()} works best if the {colors.UNDERLINE('words missing from both')}{colors.ENDC()} number is {colors.FAIL('0')}{colors.ENDC()}. I.e. the red value in the summary above."
    )
    print(
        f"\nIf you're seeing a nonzero number, maybe input 'Y' and add some words to the exceptions dictionary."
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


def save_exceptions(missing_words):
    """Save exceptions dictionary as json file."""
    json_string = json.dumps(missing_words)
    with open("../data/missing_words.json", "a+") as f:
        new_string = f.append(json_string)
        f.write(new_string)
    print("\nFile saved as missing_words.json")

def main():
    missing_words()
    exceptions = cmudict_missing()
    missing = make_exceptions_dict(exceptions)
    save_exceptions(missing_words)
    return


if __name__ == "__main__":
    main()
