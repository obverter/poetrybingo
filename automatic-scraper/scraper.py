# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# sourcery skip: for-index-underscore
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json


url = "https://www.tmz.com"
req = requests.get(url)
doc = BeautifulSoup(req.text, "html.parser")


raw_titles = doc.select("header > a > h2")


# This is a for loop that is iterating through the raw_titles list and appending
# the headlines to the headlines list.
headlines = []
valid_punct = ["'", "!", "?"]
print("\n* * * * * * * * * * Here's the latest news:* * * * * * * * * *\n")
for count, title in enumerate(enumerate(raw_titles)):
    headline = raw_titles[count].get_text().strip().replace("\n", " ") + "."
    if headline[-2] in valid_punct:
        headline = headline[:-1]
    print(headline)
    headlines.append(headline)


def get_tags(article, position):
    """
    It takes an article and a position, and returns a list of tags for that position

    :param article: the article you want to scrape
    :param position: The position of the article in the list of articles
    :return: A list of tags for the article.
    """
    tags = doc.select("section.tag-cloud > ul > a")
    tag_list = []
    for tag in tags:
        data = json.loads(tag["data-context"])
        if data["pos"] == position:
            tag_list.append(tag.text.strip())
    return tag_list


def break_timestamp(article, position):
    """
    It takes the timestamp of an article, breaks it into its component parts, and
    returns a dictionary with those parts

    :param article: the article you want to scrape
    :param position: the position of the article in the list of articles
    :return: A dictionary with the calendar, clock, year, month, day, hour, and
    minute.
    """
    timestamps = doc.select(".article")
    timestamp = timestamps[position].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()
    calendar = timestamp[:9]
    clock = timestamp[-8:].strip()
    year = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").year
    month = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").month
    day = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").day
    hour = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").hour
    minute = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").minute
    return {
        "calendar": calendar,
        "clock": clock,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
    }


break_timestamp(raw_titles, 3)


# Creating a list of tags for each article.
tags = doc.select("section.tag-cloud > ul > a")

# Creating a list of dictionaries.
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
existing = pd.read_csv("headlines.csv", index_col="Unnamed: 0")
if "tags" not in existing:
    existing["tags"] = None


# Creating a list of dataframes, and then concatenating them.
dfs = [current, existing]
existing = existing[
    ["headline", "tags", "timestamp", "year", "month", "day", "hour", "minute"]
]
export = pd.concat([current, existing])

# Sorting the dataframe by the year, month, day, hour, and minute, and then
# dropping the duplicates.
export = export.sort_values(
    by=["year", "month", "day", "hour", "minute"],
    ascending=[False, False, False, False, False],
    ignore_index=True,
)
export = export.drop_duplicates(subset=["timestamp"], keep="first", ignore_index=True)


# Writing the dataframe to a csv file.
export.to_csv("headlines.csv")
export.to_json("headlines.json")
