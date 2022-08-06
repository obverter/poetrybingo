import os, sys
#####imports####################################################################
import big_dict, loaders, syllable_counter, updater


sys.path.insert(0, "data")

#####assets#####################################################################
cmudict = loaders.load_cmu()

#####functions##################################################################

def main():
    # haiku_corpus = loaders.load_corpus()
    exceptions = loaders.load_missing()
    delta = big_dict.process_delta()
    build_dict = input("\nBuild/update your exceptions dictionary? (Y|N)\n    >  ")
    if build_dict.lower() == "n":
        print()
        print("Coward.")
        sys.exit()
    else:
        update = input("\nUPDATE the current dictionary or start from SCRATCH (U)pdate | (S)cratch | (E)xit)\n    >  ")
        if update.lower() == "u":

            missing_words_dict = updater.update()
        elif update.lower() == "s":
            print("\n")
            print(f"I think we have {len(exceptions)} words to syllabilify. Let's get started.")
            print()
            missing_words_dict = big_dict.build_dict(exceptions)
        elif update.lower() == "e":
            print("\n\n")
            print("BYE.")
            sys.exit()
        else: print("\nYou've gotta choose U or S or E.",  file=sys.stderr)
        big_dict.save_dict(missing_words_dict)


#####main#######################################################################



if __name__ == "__main__":
    main()