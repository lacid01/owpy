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

query = """
    SELECT w.timestampunx, c.cityname, w.windspeed, w.winddeg, hr.bezeichnerkurz, w.windgust, COUNT(*) as cnt,  COUNT(*)*1.0/tt.total*100 As prcnt
    FROM Wetter as w
    Inner JOIN
    (select ctyid as id, cityname FROM Cities) as c 
    ON c.id = w.ctyid 
    INNER JOIN
    (SELECT * FROM Himmelsrichtung) as hr
    ON hr.richtungsid = 1 + CAST((w.winddeg + 11.25)/22.5 AS INTEGER)
    INNER JOIN
    (
    SELECT ctyid, COUNT(*) as total FROM Wetter
    GROUP BY ctyid
    ) as tt
    ON tt.ctyid = w.ctyid
    GROUP BY c.cityname, hr.bezeichnerkurz
    ORDER BY c.cityname, hr.richtungsid
"""

data = pd.read_sql_query(query,sqlite3.connect('wetter.db'))

df = data[ (data['cityname'] == 'Michendorf') | (data['cityname'] == 'Seattle') | (data['cityname'] == 'Oslo')]

#print(df)

fig = px.line_polar(df, r="prcnt", theta="bezeichnerkurz", color="cityname", line_close=True,
                    )#color_discrete_sequence=px.colors.sequential.Plasma_r)#, template="plotly_dark",)

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