# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from math import log10
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import sqlite3
import datetime as dt
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

colors = {
    'background': '#2e4559',
    'text': '#bacbd9'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

def getCity(ctyid:int):
    id = int(ctyid)
    qr = "SELECT * FROM Cities WHERE ctyid = {} ORDER BY countrylinkage, cityname".format(id)
    return pd.read_sql_query(qr,sqlite3.connect('wetter.db'))

def getQuery(ctyid:int):
    id = int(ctyid)
    if id == 0:
        return 1
    else:
        data = getCity(ctyid)
        return data[ data['ctyid'] == id]['request'].squeeze()

def getLatLon(ctyid:int) -> list:
    id = int(ctyid)
    if id == 0:
        return [0,0]
    else:
        data = getCity(ctyid)
        return [data[ data['ctyid'] == id]['lat'].squeeze(),data[ data['ctyid'] == id]['lon'].squeeze()]

def getParallelData(ctyid:int):
    qur = """
    SELECT 
        datetime(round(w2.tss/3600/24)*3600*24, 'unixepoch') as ts, 
        round(w2.tss/3600/24)*3600*24 as ts2,
        MIN(w2.average) AS minimum, 
        MAX(w2.average) AS maximum, 
        AVG(w2.average) AS average,
        w2.windspeed,
        w2.winddeg,
        w2.winddegavg,
        w2.ctyid as ctyid, 
        w2.local,
        count(*) as cnt
    FROM 
        (
        SELECT 
            datetime(round(w.timestampunx/3600)*3600, 'unixepoch') as ts,
            round(w.timestampunx/3600)*3600 as tss, 
            AVG(w.temperature) AS average,
            AVG(w.windspeed) AS windspeed,
            AVG(w.winddeg) as winddeg,
            round(AVG(w.winddeg)/36)*36 AS winddegavg,
            w.ctyid AS ctyid,
            w.cityname AS local,
            COUNT(*)
        FROM (
            SELECT * FROM Wetter as w2
            INNER JOIN 
            (select ctyid as id, cityname FROM Cities) as c 
            ON c.id = w2.ctyid 
            WHERE c.id = """ + str(ctyid) + """) w
        GROUP BY ctyid, tss
        ) w2
    GROUP BY w2.local, ts2
    ORDER BY ts

    """
    data = pd.read_sql_query(qur,sqlite3.connect('wetter.db'))
    data['timestmp'] = data.apply(lambda x: dt.datetime.utcfromtimestamp(x['ts2']), axis=1) 
    def season (timestamp:dt.datetime) -> str:
        Monat = timestamp.month
        if (Monat > 2) and (Monat <= 5):
            return 1
        if Monat > 5 and Monat <= 8:
            return 2
        if Monat > 8 and Monat <= 11:
            return 3
        else:
            return 0

    data['season'] = data['timestmp'].apply(lambda x: season(x))
    return data[ ['average','season','windspeed','winddegavg',] ]

def getTimeseries(ctyid,days:int) -> pd.DataFrame:
    utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
    younger_than = (utc_today - (60*60*24)*days)

    if len(ctyid) < 2:
        ct = """ctyid = """ + str(ctyid[0])
    else:
        ctyidstr = [str(i) for i in ctyid]
        ct = """ctyid = """ + """ OR ctyid = """.join(ctyidstr)

    qu = "SELECT w.country, w.timestampUNX, w.timezone, w.temperature, c.cityname FROM (SELECT * FROM Wetter WHERE ({}) AND CAST(timestampUNX AS INTEGER) > CAST({} AS INTEGER)) AS w INNER JOIN (SELECT * FROM Cities) AS c ON c.ctyid = w.ctyid ORDER BY timestampUNX".format(ct, younger_than)
    data = pd.read_sql_query(qu,sqlite3.connect('wetter.db'))
    data['timestmp'] = data.apply(lambda x: dt.datetime.utcfromtimestamp(x['timestampUNX'] + x['timezone']*3600), axis=1)
    return data

def getCondition(ctyid, days:int) -> pd.DataFrame:
    print(ctyid)
    utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
    younger_than = (utc_today - (60*60*24)*days)
    if len(ctyid) < 2:
        ct = """ctyid = """ + str(ctyid[0])
    else:
        ctyidstr = [str(i) for i in ctyid]
        ct = """ctyid = """ + """ OR ctyid = """.join(ctyidstr)
    qu = """
        SELECT c.cityname, cnd.condition, COUNT(*) as cnt,  COUNT(*)*1.0/tt.total*100 As prcnt
        FROM (
        SELECT * FROM Wetter WHERE timestampunx > """ + str(younger_than) + """ AND ( """ + str(ct) + """ )
        ) as w
        Inner JOIN
            (select ctyid as id, cityname FROM Cities WHERE """ + str(ct) + """) as c 
            ON c.id = w.ctyid 
        INNER JOIN
        (SELECT * FROM conditioncode) as cnd
        ON cnd.condid = w.descrid
        INNER JOIN
        (
        SELECT tw.ctyid, COUNT(*) as total FROM (SELECT * FROM Wetter WHERE timestampunx > """ + str(younger_than) + """ AND ( """ + str(ct) + """ )) as tw
        GROUP BY ctyid
        HAVING """ + str(ct) + """
        ) as tt
        ON tt.ctyid = w.ctyid
        GROUP BY c.cityname, cnd.condition
        ORDER BY c.cityname, cnd.condition
    """
    data = pd.read_sql_query(qu,sqlite3.connect('wetter.db'))
    #data['prcnt'] = data['prcnt'].apply(lambda x: log10(x*100))
    return data


query = """
    SELECT  l.iso3166_alpha2 || ', ' || c.cityname as label, c.ctyid as value, c.request 
    FROM Cities as c 
    INNER JOIN
    (SELECT * FROM Laendercodes) as l
    ON l.id = c.countrylinkage
    ORDER BY countrylinkage, cityname
"""
data = pd.read_sql_query(query,sqlite3.connect('wetter.db'))
data['dict'] = data.apply( lambda x: { 'label': x['label'] , 'value': x['value'] }, axis = 1)
cities = [b[3] for a,b in data.iterrows()]

startvalue = cities[0]['value']

#print(df)
def getFigParallel(ctyid:int):
    df = getParallelData(ctyid)
    fig = px.parallel_coordinates(df, color="average",
                             color_continuous_scale=px.colors.diverging.Tealrose,
                             color_continuous_midpoint=2)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

def getFigTimeseries(ctyid, days:int):
    df = getTimeseries(ctyid,days)
    print(df)
    fig = px.line(df, x="timestmp", y="temperature", title='Temperatur', color='cityname', line_shape='linear')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

def getFigCondition(ctyid, days:int):
    if len(ctyid) == 0:
        print('leer')
        pass
    df = getCondition(ctyid,days)
    fig = px.line_polar(df, r="prcnt", theta="condition", color="cityname", line_close=True, log_r=True)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(style={
            'color': colors['text']
        }, children='Weather Dashboard'),


    html.Div(style={
            'color': colors['text'],
            'width': '30%', 'display': 'inline-block', 'padding': '0 20'
        }, children=[
        html.Label('Location'),
        dcc.Dropdown(
            id = 'input',
            options=cities,
            value=[startvalue],
            multi = True
        )
    ]),
    html.Br(),
    html.Div(style={
            'color': colors['text'],
            'width': '40%', 'display': 'inline-block', 'padding': '0 20'
        }, children=[
        html.Label('Data'),
        html.Div(id='lat'),
        html.Div(id='lon'),
        html.Div(id='resp'),
    ]),
    
    html.Br(),
    html.Div([
        "Days: ",
        dcc.Input(id='days', value=7, type='number')
    ]),

    html.Div(children=[
        html.Label('Location'),
        dcc.Graph( id='example-graph3'),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20', 'height': '600px'}),

    #style={'backgroundColor': colors['background']},

    html.Div(children=[
        html.Label('Location'),
        dcc.Graph( id='example-graph2'),
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div(children=[
        html.Label('Location'),
        dcc.Graph( id='example-graph'),
    ]),
    
    
    
])

@app.callback(
    [
        Output(component_id='resp', component_property='children'),
        Output(component_id='lat', component_property='children'),
        Output(component_id='lon', component_property='children'),
        Output(component_id='example-graph', component_property='figure'),
        Output(component_id='example-graph2', component_property='figure'),
        Output(component_id='example-graph3', component_property='figure'),
    ],
    [
        Input(component_id='input', component_property='value'),
        Input(component_id='days', component_property='value'),
    ]
)

def update_output_div(location,days):
    print(location)
    lat,lon = getLatLon(location[0])
    que = getQuery(location[0])
    return ['Output: {}'.format(que), 'lat: {}'.format(lat), 'lon: {}'.format(lon), getFigParallel(location[0]), getFigCondition(location,days), getFigTimeseries(location, days)]


if __name__ == '__main__':
    app.run_server(debug=True)