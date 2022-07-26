# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
from bs4 import BeautifulSoup


# %%
response = requests.get('https://www.bbc.com/')
doc = BeautifulSoup(response.text)


# %%
# Grab all of the titles
titles = doc.select(".media__title a")
titles


# %%
for title in titles:
    row = {'title': title.text.strip()}
    # link
    row['href'] = title['href']


# %%
