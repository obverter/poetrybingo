"""Produce new haiku from training corpus of existing haiku."""
import sys
import logging
import random
from collections import defaultdict
import syllable_counter


logging.disable(logging.CRITICAL)  # comment-out to enable debugging messages
logging.basicConfig(level=logging.DEBUG, format="%(message)s")


def load_training_file(file):
    """
    "Return a text file as a string."

    The first line of the function is a docstring. It's a string that describes what
    the function does. It's good practice to include docstrings in your functions

    :param file: The name of the file to load
    :return: A string of the text file.
    """

    with open(file) as f:
        return f.read()


def prep_training(raw_haiku):
    """
    > Load string, remove newline, split words on spaces, and return list

    :param raw_haiku: a string of the haiku
    :return: A list of words.
    """

    return raw_haiku.replace("\n", " ").split()


def map_word_to_word(corpus):
    """
    > The function takes a list of words and returns a dictionary of words and the
    words that follow them

    :param corpus: a list of words
    :return: A dictionary with a key of a word and a value of a list of words that
    follow that word.
    """

    limit = len(corpus) - 1
    dict1_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            suffix = corpus[index + 1]
            dict1_to_1[word].append(suffix)
    logging.debug('map_word_to_word results for "sake" = %s\n', dict1_to_1["sake"])
    return dict1_to_1


def map_2_words_to_word(corpus):
    """
    > Load list & use dictionary to map word-pair to trailing word

    :param corpus: the list of words to be used for the Markov chain
    :return: A dictionary with a key of two words and a value of a list of words
    that follow the two words.
    """
    limit = len(corpus) - 2
    dict2_to_1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = f"{word} {corpus[index + 1]}"
            suffix = corpus[index + 2]
            dict2_to_1[key].append(suffix)
    logging.debug(
        'map_2_words_to_word results for "sake jug" = %s\n', dict2_to_1["sake jug"]
    )

    return dict2_to_1


def random_word(corpus):
    """
    > Return a random word and syllable count from the training corpus

    :param corpus: a list of words
    :return: A tuple of a word and the number of syllables in that word.
    """

    word = random.choice(corpus)
    num_syls = syllable_counter.count_syl(word)
    if num_syls > 4:
        random_word(corpus)
    else:
        logging.debug("random word & syllables = %s %s\n", word, num_syls)
        return (word, num_syls)


def word_after_single(prefix, suffix_map_1, current_syls, target_syls):
    """
    It returns all acceptable words in a corpus that follow a single word

    :param prefix: the word that precedes the word we're looking for
    :param suffix_map_1: a dictionary mapping a single word to a list of words that
    follow it in the corpus
    :param current_syls: the number of syllables in the current line
    :param target_syls: the number of syllables we want in the final line
    :return: A list of words that follow the prefix and have the correct number of
    syllables.
    """

    accepted_words = []
    suffixes = suffix_map_1.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_syls = syllable_counter.count_syl(candidate)
            if current_syls + num_syls <= target_syls:
                accepted_words.append(candidate)
    logging.debug('accepted words after "%s" = %s\n', prefix, set(accepted_words))
    return accepted_words


def word_after_double(prefix, suffix_map_2, current_syls, target_syls):
    """
    It returns all acceptable words in a corpus that follow a word pair

    :param prefix: the word pair that we're looking for
    :param suffix_map_2: a dictionary of word pairs (tuples) and the words that
    follow them
    :param current_syls: the number of syllables in the current line
    :param target_syls: the number of syllables you want in your haiku
    :return: A list of words that follow the prefix and have the correct number of
    syllables.
    """

    accepted_words = []
    suffixes = suffix_map_2.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_syls = syllable_counter.count_syl(candidate)
            if current_syls + num_syls <= target_syls:
                accepted_words.append(candidate)
    logging.debug('accepted words after "%s" = %s\n', prefix, set(accepted_words))
    return accepted_words


def haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line, target_syls):
    """
    > Given a corpus, a suffix map, and a target number of syllables, build a haiku
    line

    :param suffix_map_1: a dictionary of words and the words that follow them in the
    corpus
    :param suffix_map_2: a dictionary of all the words that follow a two-word prefix
    in the corpus
    :param corpus: a list of words from the training corpus
    :param end_prev_line: the last two words of the previous line
    :param target_syls: the number of syllables in the line
    :return: A list of words that make up a line of a haiku.
    """

    line = "2/3"
    line_syls = 0
    current_line = []
    if len(end_prev_line) == 0:  # build first line
        line = "1"
        word, num_syls = random_word(corpus)
        current_line.append(word)
        line_syls += num_syls
        word_choices = word_after_single(word, suffix_map_1, line_syls, target_syls)
        while len(word_choices) == 0:
            prefix = random.choice(corpus)
            logging.debug("new random prefix = %s", prefix)
            word_choices = word_after_single(
                prefix, suffix_map_1, line_syls, target_syls
            )
        word = random.choice(word_choices)
        num_syls = syllable_counter.count_syl(word)
        logging.debug("word & syllables = %s %s", word, num_syls)
        line_syls += num_syls
        current_line.append(word)
        if line_syls == target_syls:
            end_prev_line.extend(current_line[-2:])
            return current_line, end_prev_line

    else:  # build lines 2 & 3
        current_line.extend(end_prev_line)

    while True:
        logging.debug("line = %s\n", line)
        prefix = f"{current_line[-2]} {current_line[-1]}"
        word_choices = word_after_double(prefix, suffix_map_2, line_syls, target_syls)
        while len(word_choices) == 0:
            index = random.randint(0, len(corpus) - 2)
            prefix = f"{corpus[index]} {corpus[index + 1]}"
            logging.debug("new random prefix = %s", prefix)
            word_choices = word_after_double(
                prefix, suffix_map_2, line_syls, target_syls
            )
        word = random.choice(word_choices)
        num_syls = syllable_counter.count_syl(word)
        logging.debug("word & syllables = %s %s", word, num_syls)

        if line_syls + num_syls > target_syls:
            continue
        elif line_syls + num_syls < target_syls:
            current_line.append(word)
            line_syls += num_syls
        elif line_syls + num_syls == target_syls:
            current_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(current_line[-2:])

    final_line = current_line[:] if line == "1" else current_line[2:]
    return final_line, end_prev_line


def main():
    """
    The function takes a corpus of haiku, and then creates a dictionary of suffixes
    (the last word of a line) and their corresponding prefixes (the word that comes
    before the suffix).

    The function then uses the suffix dictionary to generate a new haiku.

    The function also has the option to regenerate lines 2 and 3 of the haiku.

    The function is a bit long, but it's not too complicated.

    The first thing the function does is load the training file.

    The training file is a text file that contains a bunch of haiku.

    The function then uses the prep_training function to clean up the training file.


    The prep_training function removes punctuation, and then splits the haiku into
    lists of words.

    The function then uses the map_word_to_word function to create a dictionary of
    suffixes and their corresponding prefixes.
    """

    intro = """\n
    N-monkeys at N-typewriters for N-millenia...
            or one computer piped full of garbage
                    ...can sometimes produce a haiku.\n"""

    print(f"{intro}")
    raw_haiku = load_training_file("../data/haiku_corpus.txt")
    corpus = prep_training(raw_haiku)
    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_2_words_to_word(corpus)
    final = []
    choice = None
    while choice != "0":
        print(
            """
            TMZese Haiku Generator

            0 - Quit
            1 - Generate a TMZ Headline Haiku
            2 - Regenerate Line 2
            3 - Regenerate Line 3
            """
        )

        choice = input("Choice: ")
        print()
        if choice == "0":
            print("Coward.")
            sys.exit()
        elif choice == "1":
            final = []
            end_prev_line = []
            first_line, end_prev_line1 = haiku_line(
                suffix_map_1, suffix_map_2, corpus, end_prev_line, 5
            )

            final.append(first_line)
            line, end_prev_line2 = haiku_line(
                suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7
            )

            final.append(line)
            line, end_prev_line3 = haiku_line(
                suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5
            )

            final.append(line)
        elif choice == "2":
            if not final:
                print("I can't regenerate nothing. Try (Option 1).")
                continue
            else:
                line, end_prev_line2 = haiku_line(
                    suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7
                )

                final[1] = line
        elif choice == "3":
            if not final:
                print("I can't regenerate nothing. Try (Option 1).")
                continue
            else:
                line, end_prev_line3 = haiku_line(
                    suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5
                )

                final[2] = line
        else:
            print(
                "\nI only understand 0, 1, 2, or 3. Try one of those.", file=sys.stderr
            )
            continue
        print()
        # print("First line = ", end="")
        print(" ".join(final[0]), file=sys.stderr)
        # print("Second line = ", end="")
        print(" ".join(final[1]), file=sys.stderr)
        # print("Third line = ", end="")
        print(" ".join(final[2]), file=sys.stderr)
        print()
    input("\n\nPress the Enter key to exit.")


if __name__ == "__main__":
    main()
