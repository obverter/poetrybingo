# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
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
stories.to_csv('headlines.csv')


# %%
