import os, sys
from re import X


#####imports####################################################################
import syllable_counter, config
from loaders import load_corpus, load_cmu
from big_dict import build_dict, save_dict


#####assets#####################################################################
cmu = load_cmu()

corpus = load_corpus()

#####functions##################################################################

X
#####main#######################################################################


def update():
    try:
        with open('../data/haiku_corpus.txt') as in_file:
            corpus_path = in_file
            words = set(in_file.read().split())
    except FileNotFoundError:
        with open('../../data/haiku_corpus.txt') as in_file:
            corpus_path = in_file
            words = set(in_file.read().split())


    missing = []

    for word in words:
        try:
            num_syllables = syllable_counter.count_syl(word)
            ##print(word, num_syllables, end='\n') # uncomment to see syllable count
        except KeyError:
            missing.append(word)

    print("Missing words:", missing)

    build_dict(missing)

    save_dict(missing)

    return

if __name__ == "__main__":
    update()
    sys.exit()