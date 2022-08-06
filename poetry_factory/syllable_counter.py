"""American English syllable counter using NLTK cmudict corpus."""
import sys, os
from string import punctuation
import json
from nltk.corpus import cmudict



sys.path.insert(0, "data")

# load dictionary of words in haiku corpus but not in cmudict
try:
    with open('data/missing_words.json') as f:
        missing_words = json.load(f)
except FileNotFoundError:
    with open('../data/missing_words.json') as f:
        missing_words = json.load(f)
except FileNotFoundError:
    with open('../../data/missing_words.json') as f:
        missing_words = json.load(f)


cmudict = cmudict.dict()

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
        if word in missing_words:
            num_sylls += missing_words[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1
    return num_sylls

def main():
    while True:
        print("Syllable Counter")
        word = input("Enter word or phrase else press Enter to Exit: ")
        if word == '':
            sys.exit()
        try:
            num_syllables = count_syl(word)
            print(f"number of syllables in {word} is: {num_syllables}")
            print()
        except KeyError:
            print("Word not found.  Try again.\n", file=sys.stderr)

if __name__ == '__main__':
    main()





# from nltk.corpus import cmudict
# from string import punctuation
# import json
# import re
# import sys, os
# from loaders import load_corpus, load_cmu

# sys.path.insert(0, "data")


# corpus = load_corpus()
# cmu = load_cmu()

# def delta():
#     absentees = set()
#     for word in corpus:
#         word = word.lower().strip(punctuation)
#         if word.endswith("'s") or word.endswith("’s"):
#             word = word[:-2]
#         if word not in cmu:
#             absentees.add(word)
#         print("\nAbsentees:")
#         print(*absentees, sep='\n')
#         print(f"Words in haiku corpus: {len(corpus)}")
#         print(f"Corpus words not in CMU dictionary: {len(absentees)}")
#         included = ((len(absentees)/len(corpus)))*100
#         print(f"Percentage of words in corpus that are in CMU dictionary: {included}%")
#         return absentees

# absentees = dict(delta())

# def count_syl(word):
#     """Use corpora to count syllables in English word or phrase."""
#     # prep words for cmudict corpus
#     for word in word:
#         word = word.replace('-', ' ')
#         lower = word.lower().split()
#     num_sylls = 0
#     for word in lowers:
#         word = word.strip(punctuation)
#         if word.endswith("'s")or word.endswith("’s"):
#             word = word[:-2]
#         if word in absentees:
#             num_sylls += absentees[word]
#         else:
#             # for phonemes in cmudict[word][0]:
#             # for phonemes in current_dict[word][0]:
#             for phonemes in absentees[0]:
#                 for phoneme in phonemes:
#                     if phoneme[-1].isdigit():
#                         num_sylls += 1
#     return num_sylls

# new_adds = count_syl(absentees)

# def dump_current():
#     try:
#         with open("../data/missing_words.json", "w") as json_dict:
#                 current_dictionary = json.dump(new_adds, json_dict, indent=4)
#                 m = re.sub("[^0-9a-zA-Z]+", "", str(new_adds))
#                 current = re.sub("[^0-9a-zA-Z]+", "", str(m))
#     except FileNotFoundError:
#         with open("../../data/missing_words.json", "w") as f:
#                 missing = json.dump(missing, f, indent=4)
#                 m = re.sub("[^0-9a-zA-Z ]+", "", str(missing))
#                 current = re.sub("[^0-9a-zA-Z ]+", "", str(m))
#     return current

# def main():
#     while True:
#         print("Syllable Countifier")
#         word = input("\nEnter a word. Or a phrase works, too:\nOr you can press ENTER to exit.\n    > ")
#         if word == '':
#             print("\nSee you later, crocodile.")
#             sys.exit()
#         try:
#             num_syls = count_syl(word)
#             print(f"\n I think {word} has {num_syls} syllables.")
#             print()
#         except KeyError:
#             print("\nI have no idea what that is. Try feeding me something else.\n", file=sys.stderr)

# if __name__ == '__main__':
#     main()
