"""Find words in haiku corpus missing from cmudict & build exceptions dict."""
import sys, os
from string import punctuation
import pprint
import json
import pandas as pd
from nltk.corpus import cmudict

sys.path.insert(0, "data")
sys.path.insert(1, "haikuifier")
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

cmudict = cmudict.dict()  # Carnegie Mellon University Pronouncing Dictionary


try:
    heads = pd.read_csv("../headlines.csv")
except:
    heads = pd.read_csv("headlines.csv")




def txt_dump(heads):
    """Dump headlines to text file."""
    try:
        headlines = pd.read_csv("../headlines.csv")
    except:
        headlines = pd.read_csv("headlines.csv")
    heads = headlines['headline']
    heads = heads.str.replace("  ", "")
    heads = heads.to_list()
    lesson = lesson = " ".join(heads)
    lesson = lesson.replace(" ...", "").lower()
    lesson = lesson.replace("  ", " ")
    with open('lesson.txt', 'w') as f:
        f.write(lesson)



txt_dump(heads)

with open('../data/missing_words.json') as f:
    current_exceptions_dict = json.load(f)



def main():
    haiku = load_haiku('../data/lesson.txt')
    exceptions = cmudict_missing(haiku)
    build_dict = input("\nManually build an exceptions dictionary (y/n)? \n")
    if build_dict.lower() == 'n':
        sys.exit()
    else:
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)



def load_haiku(filename):
    """Open and return training corpus of haiku as a set."""
    with open(filename) as in_file:
        return set(in_file.read().replace('-', ' ').split())



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
    print(*exceptions, sep='\n')
    print(f"{bcolors.OKCYAN}=================================================================={bcolors.ENDC}")
    print(f"Unique words in corpus = {bcolors.OKGREEN}{len(word_set)}{bcolors.ENDC}")
    print(f"Unique words in corpus not in cmudict = {bcolors.WARNING}{len(exceptions)}{bcolors.ENDC}")
    print(f"Number of words in current exceptions dictionary = {bcolors.OKCYAN}{len(current_exceptions_dict)}{bcolors.ENDC}")
    membership = (1 - len(exceptions) / len(word_set)) * 100
    coverage = (len(current_exceptions_dict) / len(exceptions)) * 100
    missing = (len(current_exceptions_dict) - len(exceptions))
    print("Corpus cmudict membership = {:.1f}{}".format(membership, '%'))
    print("Exceptions dict coverage = {:.1f}{}".format(coverage, '%'))
    print(f"Corpus words missing from both cmudict and exceptions = {bcolors.FAIL}{missing}{bcolors.ENDC}.")
    print(f"{bcolors.OKCYAN}=================================================================={bcolors.ENDC}")
    print(f"\nThe {bcolors.OKBLUE}Haikuifier{bcolors.ENDC} works best if the {bcolors.UNDERLINE}'words missing from both'{bcolors.ENDC} number is {bcolors.FAIL}0{bcolors.ENDC}. I.e. the red value on the previous line")
    print(f"\nIf you're seeing a nonzero number, maybe input {bcolors.OKCYAN}'Y'{bcolors.ENDC} and add some words to the exceptions dictionary.")
    print(f"\nYou don't {bcolors.UNDERLINE}have{bcolors.ENDC} to.")
    print(f"\nYou don't have to do anything, really.")
    print("\nBut the generated haiku will be slightly less horrible if you do.")
    print(f"{bcolors.UNDERLINE}                      {bcolors.ENDC}")

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
    print("""
    0 - Exit & Save
    1 - Add a Word or Change a Syllable Count
    2 - Remove a Word
    """)

    while True:
        choice = input("\nEnter choice: ")
        if choice == '0':
            break
        elif choice == '1':
            word = input("\nWord to add or change: ")
            missing_words[word] = int(input(f"Enter number syllables in {word}: "))
        elif choice == '2':
            word = input("\nEnter word to delete: ")
            missing_words.pop(word, None)
    print("\nNew words or syllable changes:")
    pprint.pprint(missing_words, width=1)
    return missing_words



def save_exceptions(missing_words):
    """Save exceptions dictionary as json file."""
    json_string = json.dumps(missing_words)
    with open('../data/missing_words.json', 'w') as f:
        new_string = f.append(json_string)
        f.write(new_string)
    print("\nFile saved as ../data/missing_words.json")



if __name__ == '__main__':
    main()
