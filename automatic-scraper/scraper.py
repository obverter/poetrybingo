# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# sourcery skip: for-index-underscore
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import json
import random


url = "https://www.tmz.com"
req = requests.get(url)
doc = BeautifulSoup(req.text)


raw_titles = doc.select("header > a > h2")


headlines = []
valid_punct = ["'", "!", "?"]
for count, title in enumerate(enumerate(raw_titles)):
    print("- - -")
    headline = raw_titles[count].get_text().strip().replace("\n", " ") + "."
    if headline[-2] in valid_punct:
        headline = headline[:-1]
    print(headline)
    headlines.append(headline)


def get_tags(article, position):
    tags = doc.select("section.tag-cloud > ul > a")
    tag_list = []
    for tag in tags:
        data = json.loads(tag["data-context"])
        if data["pos"] == position:
            tag_list.append(tag.text.strip())
    return tag_list


def break_timestamp(article, position):
    timestamps = doc.select(".article")
    timestamp = timestamps[position].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()
    calendar = timestamp[:9]
    clock = timestamp[-8:].strip()
    date_a_frame = pd.DataFrame()
    year = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").year
    month = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").month
    day = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").day
    hour = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").hour
    minute = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").minute
    datetimes = {
        "calendar": calendar,
        "clock": clock,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
    }

    meta = [datetimes]
    return datetimes


break_timestamp(raw_titles, 3)


# init dataframe of tags
tags = doc.select("section.tag-cloud > ul > a")

valid_punct = ["'", "!", "?"]

dicts = []

count = 0
for article_position, article in enumerate(raw_titles, start=1):
    headline = raw_titles[count].get_text().strip().replace("\n", " ") + "."
    if headline[-2] in valid_punct:
        headline = headline[:-1]
    tag_list = get_tags(article, count + 1)

    datetimes = break_timestamp(article, count)
    timestamps = doc.select(".article")
    # grab, clean timestamp
    timestamp = timestamps[count].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()

    article_dict = {
        "headline": headline,
        "tags": tag_list,
        "timestamp": timestamp,
        "year": datetimes["year"],
        "month": datetimes["month"],
        "day": datetimes["day"],
        "hour": datetimes["hour"],
        "minute": datetimes["minute"],
    }
    dicts.append(article_dict)
    count += 1
current = pd.DataFrame(dicts)


# This is reading the headlines.csv file and converting it to a dataframe.
existing = pd.read_csv("headlines.csv")
existing = existing.dropna(axis=1).set_index("Unnamed: 0")
if "tags" not in existing:
    existing["tags"] = None
existing


dfs = [current, existing]
existing = existing[
    ["headline", "tags", "timestamp", "year", "month", "day", "hour", "minute"]
]
export = pd.concat([current, existing])

export = export.sort_values(
    by=["year", "month", "day", "hour", "minute"],
    ascending=[False, False, False, False, False],
    ignore_index=True,
)
export = export.drop_duplicates(subset=["timestamp"], keep="first", ignore_index=True)


# Now we need to instantiate a training file that we can
# run through our haikuifier.


# Here we're taking the headlines column from the export dataframe and converting it to a list.
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

with open("data/haiku_corpus.txt", "w") as f:
    f.write(corpus)
# Writing the dataframe to a csv file.
export.to_csv("headlines.csv")
export.to_json("headlines.json")
