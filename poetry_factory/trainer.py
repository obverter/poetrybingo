import os, sys

#####imports####################################################################
import big_dict, loaders, syllable_counter



#####assets#####################################################################
cmudict = loaders.load_cmu()

#####functions##################################################################

def main():
    haiku_corpus = loaders.load_haiku()
    exceptions = syllable_counter.cmu_missing(haiku_corpus)
    build_dict = input("\nBuild/update your exceptions dictionary? (Y|N) \n\n ")
    if build_dict.lower() == "n":
        print("Coward.")
        sys.exit()
    else:
        missing_words_dict = big_dict.build_dict(exceptions)
        big_dict.save_dict(missing_words_dict)


#####main#######################################################################



if __name__ == "__main__":
    main()