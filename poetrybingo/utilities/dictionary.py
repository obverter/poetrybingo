"""American English syllable counter using NLTK cmudict corpus."""
import sys
from string import punctuation
import json
import colors, corpus
import pprint

from nltk.corpus import cmudict

sys.path.insert(0, "poetrybingo/data")

def CMU():
    return cmudict.dict()

def missing_words():
    with open('poetrybingo/data/missing_words.json') as f:
        return json.load(f)


def cmudict_missing(word_set):
    """Find and return words in word set missing from cmudict."""
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
        colors.CYAN("==================================================================")
    )
    print(f"Unique words in corpus = {colors.GREEN(len(word_set))}")
    print(
        f"Unique words in corpus not in cmudict = {colors.WARNING(len(exceptions))}"
    )
    print(
        f"Number of words in current exceptions dictionary = {colors.BLUE(len(cmudict_missing()))}"
    )
    membership = (1 - len(exceptions) / len(word_set)) * 100
    coverage = (len(cmudict_missing()) / len(exceptions)) * 100
    missing = abs(len(cmudict_missing()) - len(exceptions))
    print("Corpus cmudict membership = {:.1f}{}".format(membership, "%"))
    print("Exceptions dict coverage = {:.1f}{}".format(coverage, "%"))
    print(
        f"Corpus words missing from both cmudict and exceptions = {colors.FAIL(missing)}."
    )
    print(
        colors.CYAN("==================================================================")
    )
    print(
        f"\n{colors.GREEN('Haiku Roulette')} works best if the {colors.UNDERLINE('words missing from both')} number is {colors.FAIL('0')}. I.e. the red value in the summary above."
    )
    print(
        f"\nIf you're seeing a nonzero number, maybe input 'Y' and add some words to the exceptions dictionary."
    )
    print(f"\nYou don't {colors.UNDERLINE('have')} to.")
    print(f"\nYou don't have to do anything, really.")
    print("\nBut the generated haiku will be slightly less horrible if you do.")

    return exceptions


def make_exceptions_dict(exceptions_set):
    """Return dictionary of words and syllable counts from set of words."""
    missing_words = {}
    print("Input # syllables in word. Mistakes can be corrected at end. \n")
    for word in exceptions_set:
        while True:
            num_sylls = input(f"Enter number syllables in {word}: ")
            if num_sylls.isdigit():
                break
            else:
                print("                   Not a valid answer!", file=sys.stderr)
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
    with open("missing_words.json", "w") as f:
        new_string = f.append(json_string)
        f.write(new_string)
    print("\nFile saved as missing_words.json")

def main():
    return

if __name__ == "__main__":
    main()