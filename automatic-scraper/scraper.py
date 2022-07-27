import pandas as pd
import requests
from bs4 import BeautifulSoup


url = "https://www.tmz.com"
req = requests.get(url)
doc = BeautifulSoup(req.text)


stories = []
for trash in doc.select("header > a > h2"):
    raw = trash.text
    story = {"headline": raw.strip().replace("\n", " ")}
    print(f"processing headline: {trash}")
    stories.append(story)


tmz = doc.select("header a h2")
tmz_timestamps = doc.select(".article")
stories = pd.DataFrame()
heads = []
times = []
paragraphs = []
count = 0
for trash in enumerate(tmz):
    headline = tmz[count].text
    headline = headline.replace("\n", " ")

    timestamp = tmz_timestamps[count].text.split("PT")[-20:]
    timestamp = timestamp[0][-20:]
    timestamp = timestamp.strip()

    story = {"timestamp": timestamp, "headline": headline}

    story = pd.DataFrame([story])
    stories = pd.concat([stories, story], ignore_index=True)

    count += 1

try:
    current = pd.read_csv('../headlines.csv')
    export = pd.concat([current, stories], ignore_index=True)
    export = export[['timestamp', 'headline']]
    export = export.drop_duplicates(subset ="timestamp", keep = 'first', inplace = True)
    export.to_csv('headlines.csv')
except Exception:
    current = pd.read_csv('../init.csv')
    export = pd.concat([current, stories], ignore_index=True)
    export = export[['timestamp', 'headline']]
    export = export.drop_duplicates(subset ="timestamp", keep = "first", inplace = False)
    export.to_csv('headlines.csv')
