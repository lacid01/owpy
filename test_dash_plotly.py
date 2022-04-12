# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sqlite3
import datetime as dt

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

def season (timestamp:dt.datetime) -> str:
    Monat = timestamp.month
    if (Monat > 2) and (Monat <= 5):
        return "spring"
    if Monat > 5 and Monat <= 8:
        return "summer"
    if Monat > 8 and Monat <= 11:
        return "autumn"
    else:
        return "winter"

cities = ['Michendorf','Seattle']

idx = 0
onlycities =""
for city in cities:
    if idx == 0:
        onlycities += "c.cityname = '" + city + "'"
        idx += 1
    else:
        onlycities += " OR c.cityname = '" + city + "'"

query = "SELECT w.wetterid, w.country, w.city, c.cityname as ziel, w.timestampunx, datetime(w.timestampunx, 'unixepoch') AS timestmp, w.temperature,w.temperaturegefuehlt,w.humidity, w.pressure, w.windspeed, w.rain1h, w.cloudiness, w.timezone, w.sunrise, w.sunset FROM Wetter as w INNER JOIN (select ctyid as id, cityname FROM Cities) as c ON c.id = w.ctyid WHERE (" + onlycities + ") ORDER BY w.timestampUNX"

data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
data['timestmp'] = data.apply(lambda x: dt.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=(60*60*x['timezone'])),axis=1) 
data['season'] = data['timestmp'].apply(lambda x : season(x))

df = data

#print(df)

fig = px.box(df, x="season", y="temperature", color="ziel")#, barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)