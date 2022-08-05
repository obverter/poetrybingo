import os, sys


#####imports####################################################################
import loaders, syllable_counter, config
from config import relpath as relpath


#####assets#####################################################################
cmudict = loaders.load_cmu()

corpus = loaders.load_haiku()

#####functions##################################################################


#####main#######################################################################
try:
    with open('../data/haiku_corpus.txt') as in_file:
        words = set(in_file.read().split())
except FileNotFoundError:
    with open('../../data/haiku_corpus.txt') as in_file:
        words = set(in_file.read().split())
finally:
    print(f"Working off of {relpath(__file__)}")

missing = []

for word in words:
    try:
        num_syllables = syllable_counter.count_syl(word)
        ##print(word, num_syllables, end='\n') # uncomment to see syllable count
    except KeyError:
        missing.append(word)

print("Missing words:", missing, file=sys.stderr)
