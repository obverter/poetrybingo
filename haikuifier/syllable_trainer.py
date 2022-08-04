"""Find words in haiku corpus missing from cmudict & build exceptions dict."""

import sys
from string import punctuation
import pprint
import json
import pandas as pd
from nltk.corpus import cmudict
from loaders import (
    bcolors,
    whats_new,
    get_cmu,
    get_haiku_corpus,
    get_headlines,
    get_trainer,
    get_current_exceptions,
    cmudict_missing,
)
from user_actions import main, make_exceptions_dict, save_exceptions


cmudict = get_cmu()

haiku = get_haiku_corpus()

headlines = get_headlines()

current_exceptions_dict = get_current_exceptions()

trainer = get_trainer()


cmu = list(cmudict.keys())


new = whats_new()


if __name__ == "__main__":
    main()
