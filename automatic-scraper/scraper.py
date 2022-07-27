# sourcery skip: for-index-underscore
import contextlib
import pandas as pd
import requests
from datetime import *
from bs4 import BeautifulSoup


url = "https://www.tmz.com"
req = requests.get(url)
doc = BeautifulSoup(req.text)


# init var headline
tmz = doc.select("header a h2")


# init var timestamp
tmz_timestamps = doc.select(".article")


# main loop
stories = pd.DataFrame()
paragraphs = []
count = 0

for trash in enumerate(tmz):
    # grab headline text
    headline = tmz[count].text
    headline = headline.replace("\n", " ")

    # grab, clean timestamp
    timestamp = tmz_timestamps[count].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()

    # set timestamp, date, time, headlie
    story = {
        "timestamp": timestamp,
        "date": timestamp[:9],
        "time": timestamp[-8:].strip(),
        "headline": headline,
    }

    # convert to df
    story = pd.DataFrame([story])


    story.convert_dtypes()

    story["year"] = pd.DatetimeIndex(story["date"]).year
    story["month"] = pd.DatetimeIndex(story["date"]).month
    story["day"] = pd.DatetimeIndex(story["date"]).day
    story["hour"] = pd.DatetimeIndex(story["time"]).hour
    story["minute"] = pd.DatetimeIndex(story["time"]).minute
    # parse date into columns
    # try:
    #     story["year"] = story['date'].astype(str)[-4:]
    # except:
    #     story["year"] = story["year"]

    # append story to raw stories df to be merged with historical df
    stories = pd.concat([stories, story], ignore_index=True)

    count += 1

stories = stories[["headline", "timestamp", "year", "month", "day", "hour", "minute"]]

existing = pd.read_csv("headlines.csv")
existing = existing.dropna(axis=1).set_index("Unnamed: 0")
existing.convert_dtypes()

existing["year"] = pd.DatetimeIndex(existing["timestamp"]).year
existing["month"] = pd.DatetimeIndex(existing["timestamp"]).month
existing["day"] = pd.DatetimeIndex(existing["timestamp"]).day
existing["hour"] = pd.DatetimeIndex(existing["timestamp"]).hour
existing["minute"] = pd.DatetimeIndex(existing["timestamp"]).minute

try:
    existing = pd.read_csv("headlines.csv")
    existing.convert_dtypes()
    existing["year"] = pd.DatetimeIndex(existing["timestamp"]).year
    existing["month"] = pd.DatetimeIndex(existing["timestamp"]).month
    existing["day"] = pd.DatetimeIndex(existing["timestamp"]).day
    existing["hour"] = pd.DatetimeIndex(existing["timestamp"]).hour
    existing["minute"] = pd.DatetimeIndex(existing["timestamp"]).minute
    existing = existing[
        [
            "headline",
            "timestamp",
            "date",
            "time",
            "year",
            "month",
            "day",
            "hour",
            "minute",
        ]
    ]
except:
    print("try failed")

export = pd.concat([existing, stories], ignore_index=True)
export.convert_dtypes()
export = export[["headline", "timestamp", "year", "month", "day", "hour", "minute"]]
export.to_csv("headlines.csv")
