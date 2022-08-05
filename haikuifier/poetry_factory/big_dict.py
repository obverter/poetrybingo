import json
import re
import sys
import pprint

sys.path.insert(0, "haikuifier/poetry_factory/")

def build_dict(exceptions_set):
    missing = {}
    print("How many syllables are in these words?\nYou can fix mistakes later if/when you make any. \n")

    for word in exceptions_set:
        while True:
            num_syllables = input(f"How many syllables are in {word}: ")
            if num_syllables.isdigit():
                break
            else:
                print("FEED ME NUMBERS, FEED ME NUMBERS, FEED ME NUMBERS.\nPlease enter an integer. An integer is a number with no decimal points.\n", file=sys.stderr)

        missing[word] = int(num_syllables)
    print()
    pprint.pprint(missing, width=1)
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
    pprint.pprint(missing, width=1)
    return missing

def save_dict(missing):
    json_string = json.dumps(missing)
    with open("data/addenda.json", "w") as f:
        f.write(json_string)
    print("\nYour dictionary has been saved @ data/addenda.json\n")


if __name__ == "__main__":
    main()