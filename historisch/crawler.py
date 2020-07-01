import pandas as pd
from requests_html import HTMLSession,HTML
from pprint import pprint
import sys, json, requests, sqlite3
import datetime as dt
from html.parser import HTMLParser
import html as hhtml



f = open("./historisch/brandenburg.html", "r")
doc = f.read()

html = HTML(html=doc)


dfs = pd.read_html("./historisch/brandenburg.html", thousands='.', decimal=",")

months = ['Januar','Februar','Maerz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']

data = pd.DataFrame()

_df = dfs[0]
_df = _df.set_index('JahrYear').rename(columns={"WertValue":"Januar"})

data = _df

idx = 0
for df in dfs:
    if idx == 0:
        idx = 1
    else:
        _df = df
        _df = _df.set_index('JahrYear').rename(columns={"WertValue": months[idx]})
        #print(_df)
        data = pd.merge(data, _df, left_index=True, right_index=True, how='outer')
        idx = idx + 1

print(data.T)