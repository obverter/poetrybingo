#### system imports ############################################################
import sys, os

sys.path.insert(0, "poetry_factory")


#### poetry imports ############################################################
from poetry_factory import (
    big_dict,
    loaders,
    syllable_counter as sylcount,
    trainer,
    haikuifier as haiku,
    updater,
)

#### pseudo ####################################################################

'''
Init
Show delta of dictionary (CMU + ADDENDA.JSON = DICT) and unique words in corpus (CORPUS)
> Build/Update DICT? (Y|N)
    Y: Build/Update DICT
        > EDIT-DICT: Edit/Update DICT or start over? (E|S)
            E: [[__EDIT-DICT__]]
                Pull '∆CORPUS(DICT)' into trainer ([[__DELTA__]])
                > Train
                > Fix/Save/Exit without saving?
                    Fix: GOTO [[__EDIT-DICT__]]
                    Save: GOTO [[__SAVE-DICT__]]
                        [[__SAVE-DICT__]] Save/Overwrite DICT to 'ADDENDA.JSON'
                        > Poetry/Edit/Exit? (P|Ed|Ex)
                            P: GOTO [[__POETRY__]]
                            Ed: GOTO [[__EDIT-DICT__]]
                            Ex: GOTO [[__EXIT__]]
                    Exit: GOTO [[__EXIT__]]
            S: Start over
                Pull '∆CORPUS(DICT)' into [[__TRAINER__]]
                > Train
                > DICT: Fix/Save+Exit/Exit without saving?
                    Fix: GOTO [[__EDIT-DICT__]]
                    Save: Save dict to 'ADDENDA.JSON'
                        > Poetry? (Y|N)
                            Y: GOTO [[__POETRY__]]
                            N: Exit
    N: Poetry/Flee? (P|F)
        P: GOTO [[__POETRY__]]
        F: GOTO [[__EXIT__]]
> Kinda poetry we doin (Haku|Exit)
    Haku: GOTO [[__HAIKU__]]
        [[__HAIKU__]] 1. GENERATE 2. CHANGE L2 3. CHANGE L3 4. EXIT (1|2|3|4)
            1. GOTO [[__GENERATE__]]
                [[__GENERATE__]]

    Exit: GOTO [[__EXIT__]]



'''



#### functions #################################################################

def delta(corpus):
    with open('../data/haiku_corpus.txt') as in_file:
        words = set(in_file.read().split())

    missing = []

    for word in words:
        try:
            num_syllables = sylcount(word)
            ##print(word, num_syllables, end='\n') # uncomment to see syllable count
        except KeyError:
            missing.append(word)






#### main ######################################################################
