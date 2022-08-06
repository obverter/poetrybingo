import sys
import json
import pprint
from loaders import bcolors, whats_new, get_cmu, get_haiku_corpus, get_headlines, get_trainer, get_current_exceptions, load_haiku, cmudict_missing

new = whats_new()

def main():
    """
    > The function `main()` prompts the user to either build a new exceptions
    dictionary from scratch, update an existing exceptions dictionary, or flee
    """
    haiku = load_haiku("../data/lesson.txt")
    exceptions = cmudict_missing(haiku)
    build_dict = input(
        f"\n\n    1. Manually {bcolors.OKGREEN}build{bcolors.ENDC} an exceptions dictionary from scratch \n\n    2. Manually {bcolors.OKCYAN}update{bcolors.ENDC} the existing exceptions dictionary \n\n    3. {bcolors.FAIL}Flee{bcolors.ENDC}\n\n{bcolors.OKBLUE}[1|2|3]{bcolors.ENDC}: {bcolors.OKGREEN}> {bcolors.ENDC}"
    )

    if build_dict.lower() == "3":
        print("")
        print("Coward.")
        sys.exit()
    elif build_dict.lower() == "2":
        missing_words_dict = update_exceptions_dict(exceptions)
    elif build_dict.lower() == "1":
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)
    else:
        print("\n\nPlease enter a valid option.", file=sys.stderr)

def make_exceptions_dict(exceptions_set):
    """
    The function takes a set of words as input and returns a dictionary of words and
    syllable counts

    :param exceptions_set: a set of words that are not in the CMU dictionary
    :return: A dictionary of words and syllable counts from a set of words.
    """

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
    print(missing_words)
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
    print(missing_words)
    return missing_words

def update_exceptions_dict(exceptions_set):
    """
    The function takes a set of words and returns a dictionary of words and syllable
    counts

    :param exceptions_set: a set of words that are not in the exceptions dictionary
    :return: A dictionary of words and syllable counts.
    """
    current_exceptions = get_current_exceptions()
    missing_words = {}
    print("Input # syllables in word. Mistakes can be corrected at end. \n")
    for count, word in enumerate(new, start=1):
        while True:
            num_sylls = input(f"Enter number syllables in {word}: ")
            if num_sylls.isdigit():
                break
            else:
                print("                   Not a valid answer!", file=sys.stderr)
        missing_words[f"{len(current_exceptions)} + {count}"] = int(num_sylls)
    print()
    print(missing_words)
    print("\nMake Changes to Dictionary Before Saving?")
    print("""
    0 - Exit & Save
    1 - Add a Word or Change a Syllable Count
    2 - Remove a Word
    """)

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
    print(missing_words)
    return missing_words


def save_exceptions(missing_words):
    """
    It takes a dictionary of missing words and saves it as a json file

    :param missing_words: a dictionary of words that are missing from the dictionary
    """

    json_string = json.dumps(missing_words)
    updated_string = json_string + missing_words
    with open("../data/missing_words_update.json", "w") as f:
        updated_string = f.append(updated_string)
        f.write(updated_string)
    print("\nFile saved as ../data/missing_words.json")