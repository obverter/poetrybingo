import contextlib
from random import sample
import pandas as pd
import pathlib
from pathlib import Path
import re
import sys, os


sys.path.append(os.path.join(sys.path[0],'poetrybingo', 'utilities'))
sys.path.append(os.path.join(sys.path[0],'poetrybingo', 'data'))
sys.path.append(os.path.join(sys.path[0],'poetrybingo', 'modules'))


def get_headlines():
    return pathlib.Path("../data/headlines.csv").read_text()


def load_corpus():
    with open("../data/corpus.txt", "r+") as f:
        return f.read()




def txt_dump():
    """Dump headlines to text file."""
    headlines = pd.read_csv("../data/headlines.csv")
    heads = headlines["headline"]
    corpus = heads.to_list()
    with contextlib.suppress(AttributeError):
        corpus = [word.replace(" ...", "").lower() for word in corpus]
        corpus = re.sub(r"[^a-zA-Z0-9 !?]", " ", corpus)
        return corpus
    flat = corpus
    with contextlib.suppress(TypeError):
        flat = [item for sublist in flat for item in sublist]
    with open("../data/heads.txt", "r+") as f:
        f.write(str(flat))


def shuffle_corpus():
    with open("../data/heads.txt", "r+") as f:
        heads = f.read()
    seed = heads.lower().split()
    mix1 = sample(seed, len(seed))
    mix2 = sample(seed, len(seed))
    mix3 = sample(seed, len(seed))
    mix4 = sample(seed, len(seed))
    mix5 = sample(seed, len(seed))
    mix6 = sample(seed, len(seed))
    mix7 = sample(seed, len(seed))
    mix8 = sample(seed, len(seed))
    mix9 = sample(seed, len(seed))
    with open("../data/corpus.txt", "w") as f:
        corpus = f"{seed}{mix1}{mix2}{mix3}{mix4}{mix5}{mix6}{mix7}{mix8}{mix9}"
        corpus = corpus.strip()
        corpus = re.sub("[^\w -]", "", corpus)
        corpus = " ".join(corpus.split())
        f.write(corpus)
    return


def main():
    txt_dump()
    shuffle_corpus()


if __name__ == "__main__":
    main()
