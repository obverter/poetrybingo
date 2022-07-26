# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


# %%
url = 'https://www.tmz.com'
req = requests.get(url)
doc = BeautifulSoup(req.text)


# %%
stories = {}
for trash in doc.select('header > a > h2'):
        raw = trash.text
        story = {
                "headline": raw.strip().replace("\n", " ")
        }
        stories |= story
stories


# %%
tmz = doc.select('header a h2')
tmz_timestamps = doc.select(".article")
stories = pd.DataFrame(columns=["timestamp", "headline"])
paragraphs = []
count = 0
for trash in enumerate(tmz):
    headline = tmz[count].text
    headline = headline.replace("\n", " ").upper()

    timestamp = tmz_timestamps[count].text.split('PT')[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()

    story = {
        "timestamp": timestamp,
        "headline": headline
    }

    stories = stories.append(story, ignore_index=True)
    count += 1


# %%
pp = tmz_timestamps[0].text.split('PT')[-20:]
pp = pp[0][-20:]
pp = pp.strip()
pp


# %%
stories


# %%
stories = pd.DataFrame(columns=['headline', 'timestamp', 'text'])
tmz = doc.select(".article")
paragraphs = []
count = 0
for count, p in enumerate(tmz):
    para = tmz[count].text
    para = para.strip().replace("\n", " ")
    paragraphs.append(para)

    headline = paragraphs[0].split("PT")

    text = headline[1]

    timestamp = headline[0][-20:]
    timestamp = timestamp.strip()

    headline = headline[0][:-20]
    headline = headline.split("  ")
    headline = headline[0].upper()

    story = {
        "headline": headline,
        "timestamp": timestamp,
        "text": text
    }
    stories = stories.append(story, ignore_index = True)
    count += 1
stories.head()
# print(headline)
# print(timestamp)
# print(test)


# %%



# %%
story['text'] = story['text'].strip()


# %%
story['text'] = story


# %%
stories = stories.append(story, ignore_index=True)
stories.head()


# %%
import sidetable


# %%
def generalize(ser, match_name, default=None, regex=False, case=False):
    """ Search a series for text matches.
    Based on code from https://www.metasnake.com/blog/pydata-assign.html

    ser: pandas series to search
    match_name: tuple containing text to search for and text to use for normalization
    default: If no match, use this to provide a default value, otherwise use the original text
    regex: Boolean to indicate if match_name contains a  regular expression
    case: Case sensitive search

    Returns a pandas series with the matched value

    """
    seen = None
    for match, name in match_name:
        mask = ser.str.contains(match, case=case, regex=regex)
        if seen is None:
            seen = mask
        else:
            seen |= mask
        ser = ser.where(~mask, name)
    ser = ser.where(seen, default) if default else ser.where(seen, ser.values)
    return ser


# %%
