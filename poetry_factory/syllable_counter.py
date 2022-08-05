
from nltk.corpus import cmudict
from string import punctuation
import json
import re
import sys
import loaders


corpus = loaders.load_haiku()

def delta():
    exceptions = set()
    for word in corpus:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if word not in cmudict:
            exceptions.add(word)
        print("n\exceptions:")
        print(*exceptions, sep='\n')
        print(f"Words in haiku corpus: {len(corpus)}")
        print(f"Corpus words not in CMU dictionary: {len(exceptions)}")
        included = ((len(exceptions)/len(corpus)))*100
        print(f"Percentage of words in corpus that are in CMU dictionary: {included}%")
        return exceptions

missing_words = delta(corpus)

def dump_current():
    with open("missing_words.json", "w") as f:
        missing_words = json.dump(missing_words, f)
        missing = re.sub("[^0-9a-zA-Z]+", "", str(missing_words))
    return missing

missing = dump_current()

def count_syl(words):
    """Use corpora to count syllables in English word or phrase."""
    # prep words for cmudict corpus
    words = words.replace('-', ' ')
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s")or word.endswith("’s"):
            word = word[:-2]
        if word in missing:
            num_sylls += missing[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1
    return num_sylls

def main():
    while True:
        print("Syllable Countifier")
        word = input("\nEnter a word. Or a phrase works, too:\nOr you can press ENTER to exit.\n    > ")
        if word == '':
            print("\nSee you later, crocodile.")
            sys.exit()
        try:
            number_of_syllables = count_syl(word)
            print(f"\n I think {word} has {number_of_syllables} syllables.")
            print()
        except KeyError:
            print("\nI have no idea what that is. Try feeding me something else.\n", file=sys.stderr)

if __name__ == '__main__':
    main()
