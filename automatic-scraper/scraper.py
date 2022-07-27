import pandas as pd
import requests
from bs4 import BeautifulSoup

# Grab trash
url = "https://www.tmz.com"
req = requests.get(url)
doc = BeautifulSoup(req.text)

tmz = doc.select("header a h2")
tmz_timestamps = doc.select(".article")
stories = pd.DataFrame(columns=["timestamp", "headline"])
new_stories = pd.DataFrame(columns=["timestamp", "headline"])
paragraphs = []
count = 0
for _ in enumerate(tmz):
    # Grab headline
    headline = tmz[count].text
    headline = headline.replace("\n", " ").upper()

    # Grab timestamp
    timestamp = tmz_timestamps[count].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()

    # Prep for append
    story = {"timestamp": [timestamp], "headline": [headline]}

    # append
    new_stories |= story

    count += 1

try:
    # Pull current headlines.csv
    current = pd.read_csv("headlines.csv")
except Exception:
    # Init headlines.csv if it doesn't exist
    current = pd.DataFrame(columns=["timestamp", "headline"])

merge = pd.concat([current, new_stories], ignore_index=True)
merge = merge[["timestamp", "headline"]]

merge.to_csv("headlines.csv")
