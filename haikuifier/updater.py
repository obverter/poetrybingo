import os, sys

sys.path.insert(0, "haikuifier/poetry_factory")

#####imports####################################################################
from poetry_factory import big_dict, loaders, syllable_counter


#####assets#####################################################################
cmudict = loaders.load_cmu()

#####functions##################################################################


#####main#######################################################################

with open('haiku_corpus.txt.') as in_file:
    words = set(in_file.read().split())

missing = []

for word in words:
    try:
        num_syllables = syllable_counter.count_syl(word)
        ##print(word, num_syllables, end='\n') # uncomment to see syllable count
    except KeyError:
        missing.append(word)

print("Missing words:", missing, file=sys.stderr)




if __name__ == "__main__":
    main()