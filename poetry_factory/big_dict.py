import json
from json import JSONEncoder
import re
import sys
import loaders, syllable_counter
from deepdiff import DeepDiff
from syllable_counter import count_syl
from deepdiff import grep
from pprint import PrettyPrinter

from tqdm import tqdm


pp = PrettyPrinter(indent=4)

sys.path.insert(0, "data")

corpus = loaders.load_corpus()
cmu = loaders.load_cmu()

def process_delta():
    try:
        with open('data/haiku_corpus.txt') as ingest:
            words = list(set(ingest.read().split()))
    except:
        with open('../data/haiku_corpus.txt') as ingest:
            words = list(set(ingest.read().split()))
    try:
        with open('data/missing_words.json') as f:
            missing = json.load(f)
    except:
        with open('../data/missing_words.json') as f:
            missing = json.load(f)

    current_known = set((list(missing.keys())) + list(cmu.keys()))

    absentees = [word for word in tqdm(words) if word not in current_known]

    # for word in words:
    #     if word in missing:
    #         try:
    #             num_syllables = count_syl(word)
    #         except KeyError:
    #             absentees.append(word)
    #     else:
    #         absentees.append(word)
    print("These words aren't in the Syllable Dictionary:")
    print(absentees)
    print(f"\nThere are {len(absentees)} of them.\n")
    return absentees

try:
    with open('data/missing_words.json') as f:
        missing = json.load(f)
except:
    with open('../data/missing_words.json') as f:
        missing = json.load(f)

current_known = set((list(missing.keys())) + list(cmu.keys()))

class set_encoder(JSONEncoder):
    def default(self, obj):
        return list(obj)

current = set_encoder().encode(current_known)

absents = process_delta()

absent = json.dumps(absents)

def build_dict(exceptions_set):
    missing = {}
    print('''
          I'm gonna go through list of words that are in the headline corpus
          that are missing from my syllable dictionary, and I'm gonna show them
          to you one by one.

          Your job is to tell me how many syllables each one has. This is
          important because I'm a computer, and computers can't read;
          we're just really good at faking it.

          Like take for example the word 'moped'. Is it one syllable or two?

          'I moped around town on my moped.'

          I have no idea. But you do.

          And what about Kanye? Or Beyoncé? Or Danny DeVito? The dictionary I
          was born with has never heard of them. But you have.
          ''')
    print("\nSo how many syllables are in these words?\nYou can fix mistakes later if/when you make any. \n")

    for word in exceptions_set:
        while True:
            num_syllables = input(f"How many syllables are in {word.upper()}: ")
            if num_syllables.isdigit():
                break
            else:
                print("FEED ME NUMBERS, FEED ME NUMBERS, FEED ME NUMBERS.\nPlease enter an integer. An integer is a number with no decimal points.\n", file=sys.stderr)

        missing[word] = int(num_syllables)
    print()
    print(missing, width=1)
    print("\nWanna make any changes to your dictionary before saving?")
    print("""
    0: Save and exit
    1: Add a word to the dictionary
    2: Remove a word from the dictionary
    """)

    while True:
        choice = input("\nChoose wisely:\n    > ")
        if choice == '0':
            print("Saved! Take it easy.")
            break
        elif choice == '1':
            word = input("\nWhat word do you want to add or change?\n    > ")
            missing[word] = int(input(f"How many syllables are in {word}: "))
        elif choice == '2':
            word = input("\nWhat word do you want to remove?\n    > ")
            missing.pop(word, None)
    print("\nYour dictionary has been updated.\n Here's what's new:")
    print(missing)
    return missing

def save_dict(missing):
    new_additions = json.dumps(missing)
    try:
        with open("data/addenda.json", "w") as f:
            f.write(new_additions)
    except Exception:
        with open("../data/addenda.json", "w") as f:
            f.write(new_additions)
    print("\nYour dictionary has been saved @ data/addenda.json\n")
    return new_additions

def merge_new(new_additions):
    dictA = json.loads(new_additions)
    dictB = json.loads(current)

    merged_dict = dict(dictA.items() + dictB.items())

    # string dump of the merged dict
    jsonString_merged = json.dumps(merged_dict)

    try:
        with open("data/addenda2.json", "w") as f:
            f.write(new_additions)
    except Exception:
        with open("../data/addenda2.json", "w") as f:
            f.write(new_additions)
    print("\nYour dictionary has been saved @ data/addenda2.json\n")
