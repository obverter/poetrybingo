import re
import json
import random

lesson = export["headline"].to_list()

# Taking the list of headlines and converting it to a clean string.
flattened = ", ".join(lesson).replace(" ...", "")
flattened = flattened.replace(".", "")
flattened = flattened.replace(",", "").lower()
flattened = flattened.replace("!", "").lower()
flattened = flattened.split(" ")
filtered = [element for element in flattened if element != None]

def blend(filtered, times):
    out = []
    for _ in range(times):
        blend = random.sample(filtered, len(filtered))
        out.append(blend)
    flat = [item for sublist in out for item in sublist]

    return [element for element in flat if element != None]

corpus = blend(filtered, 4)

corpus = " ".join(corpus)

def dump_haiku(corpus):
    with open("data/haiku_corpus.json", "w") as f:
        haiku_json = json.dump(corpus, f)
        haiku_json = re.sub("[^0-9a-zA-Z]+", "", str(haiku_json))
    return json.load(f)

dump_haiku()