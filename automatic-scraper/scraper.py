# sourcery skip: for-index-underscore
import contextlib
import pandas as pd
import requests
from datetime import *
from bs4 import BeautifulSoup


# This is a web scraper. It is grabbing the html from the TMZ website.
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

    # set timestamp, date, time, headline
    story = {
        "timestamp": timestamp,
        "date": timestamp[:9],
        "time": timestamp[-8:].strip(),
        "headline": headline,
    }

    # convert to df
    story = pd.DataFrame([story])

    # convert story 12AP to 24
    try:
        story["time"] = pd.to_datetime(story["time"], format="%I:%M %p").dt.strftime(
            "%H:%M"
        )
    except Exception:
        story["time"] = story["time"]

    story.convert_dtypes()

    # Parsing the date and time into columns.
    story["year"] = pd.DatetimeIndex(story["date"]).year
    story["month"] = pd.DatetimeIndex(story["date"]).month
    story["day"] = pd.DatetimeIndex(story["date"]).day
    story["hour"] = pd.DatetimeIndex(story["time"]).hour
    story["minute"] = pd.DatetimeIndex(story["time"]).minute

    # append story to raw stories df to be merged with historical df
    stories = pd.concat([stories, story], ignore_index=True)

    count += 1

# Creating a new dataframe with the columns headline, timestamp, year, month, day,
# hour, and minute.
stories = stories[["headline", "timestamp", "year", "month", "day", "hour", "minute"]]


# This is reading the headlines.csv file and converting it to a dataframe.
existing = pd.read_csv("headlines.csv")
existing = existing.dropna(axis=1).set_index("Unnamed: 0")
existing.convert_dtypes()

# Parsing the timestamp into columns.
existing["year"] = pd.DatetimeIndex(existing["timestamp"]).year
existing["month"] = pd.DatetimeIndex(existing["timestamp"]).month
existing["day"] = pd.DatetimeIndex(existing["timestamp"]).day
existing["hour"] = pd.DatetimeIndex(existing["timestamp"]).hour
existing["minute"] = pd.DatetimeIndex(existing["timestamp"]).minute

# This is a try/except block. It is trying to read the headlines.csv file and
# convert it to a dataframe with time-parsed columns. If it fails, it will pass.
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
except Exception:
    pass

# This is concatenating the existing dataframe with the new dataframe.
export = pd.concat([existing, stories], ignore_index=True)
export = export[["headline", "timestamp", "year", "month", "day", "hour", "minute"]]

# Dropping duplicates and sorting the dataframe by year, month, day, hour, and
# minute.
export = export.drop_duplicates(subset=["timestamp"], keep="last")
export = export.sort_values(
    by=["year", "month", "day", "hour", "minute"],
    ascending=[False, False, False, False, False],
    ignore_index=True,
)

# Writing the dataframe to a csv file.
export.to_csv("headlines.csv")
export.to_json("headlines.json")
