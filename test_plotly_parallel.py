import plotly.express as px
import pandas as pd
import sqlite3
import datetime as dt

query = """
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
        WHERE cityname = 'Schöneberg') w
  	  GROUP BY ctyid, tss
    ) w2
GROUP BY w2.local, ts2
ORDER BY ts

"""

data = pd.read_sql_query(query,sqlite3.connect('wetter.db'))

print('Starte Zeitstempelumrechnung...')
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

print(data)



df = data[ ['average','season','windspeed','winddegavg','cnt',] ]
fig = px.parallel_coordinates(df, 
                             color_continuous_scale=px.colors.diverging.Tealrose,
                             color_continuous_midpoint=2) #color="local",
fig.show()