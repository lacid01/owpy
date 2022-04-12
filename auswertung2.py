import pandas as pd
import sqlite3
from dbhelper import getTableSelect
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns



'''
Aggregiere erst auf Stunden Ebene, danach auf Tagesebe für bessere Ergebnisse bei Durchschnittsabfragen

SELECT 
	datetime(round(w2.tss/3600/24)*3600*24, 'unixepoch') as ts, 
    round(w2.tss/3600/24)*3600*24 as ts2,
    MIN(w2.average) AS minimum, 
    MAX(w2.average) AS maximum, 
    AVG(w2.average) AS average,
    w2.ctyid as ctyid, 
    w2.local,
    count(*) as cnt
FROM 
	(
      SELECT 
  		datetime(round(w.timestampunx/3600)*3600, 'unixepoch') as ts,
		round(w.timestampunx/3600)*3600 as tss, 
    	AVG(w.temperature) AS average,
      	w.ctyid AS ctyid,
        w.cityname AS local,
        COUNT(*)
	  FROM (
        SELECT * FROM Wetter as w2
        INNER JOIN 
        (select ctyid as id, cityname FROM Cities) as c 
        ON c.id = w2.ctyid 
        WHERE cityname = 'Schöneberg' or cityname = 'Seattle') w
  	  GROUP BY ctyid, tss
    ) w2
GROUP BY w2.local, ts2
ORDER BY ts

#####

Nur Stundenebene aggregiert:

      SELECT 
  		datetime(round(w.timestampunx/3600)*3600, 'unixepoch') as ts,
		round(w.timestampunx/3600)*3600 as tss, 
    	w.temperature,
      	w.ctyid,
        w.cityname,
        COUNT(*)
	  FROM (
        SELECT * FROM Wetter as w2
        INNER JOIN 
        (select ctyid as id, cityname FROM Cities) as c 
        ON c.id = w2.ctyid 
        WHERE cityname = 'Schöneberg' or cityname = 'Seattle') w
  	  GROUP BY ctyid, tss



'''



#%%
cities = ['Michendorf','Bad Belzig','Schöneberg']
#cities = ['Michendorf','Bad Belzig','München Aubing']
#cities = ['Oslo','Al']
#cities = ['Grundtjärn','Stockholm','Umea']
#cities = ['Sonderburg','Nordborg','Nyborg']
#cities = ['Goroka','Boram','Aitape']
#cities = ['Eagle, Colorado','Naples, FL','Houston, Texas','Moscow']
#cities = ['Seattle','Moscow','Quillayute Airport-UIL']
days = 7
#%%


utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
younger_than = (utc_today - 60*60*24*days)

idx = 0
onlycities =""
for city in cities:
    if idx == 0:
        onlycities += "c.cityname = '" + city + "'"
        idx += 1
    else:
        onlycities += " OR c.cityname = '" + city + "'"

query = "SELECT w.wetterid, w.country, w.city, c.cityname as ziel, w.timestampunx, datetime(w.timestampunx, 'unixepoch') AS timestmp, w.temperature,w.temperaturegefuehlt,w.humidity, w.pressure, w.windspeed, w.rain1h, w.cloudiness, w.timezone, w.sunrise, w.sunset FROM Wetter as w INNER JOIN (select ctyid as id, cityname FROM Cities) as c ON c.id = w.ctyid WHERE (" + onlycities + ") AND CAST(w.timestampunx AS INTEGER) > CAST(" + str(younger_than) + " AS INTEGER) ORDER BY w.timestampUNX"
#data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
print('Starte db-Abfrage...')
data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
print(str(data.size) + "/10 Daten abgefragt")
#print('Reduziere Datensatz...')
#utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
#data = data[ data['timestampUNX'] > (utc_today - 60*60*24*days) ]
print('Starte Zeitstempelumrechnung...')
data['timestmp'] = data.apply(lambda x: dt.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=(60*60*x['timezone'])),axis=1) 

def tagnacht(ts,tssunr,tssuns):
    if ts > tssunr and ts < tssuns:
        return "Tag"
    else:
        return "Nacht"

#data['windspeed'] = (data['windspeed'].fillna(method='ffill')).rolling(10, min_periods=1).mean()
#data['windgust'] = (data['windgust'].fillna(method='ffill')).rolling(10, min_periods=1).mean()
data['rain1h'] = data['rain1h'].fillna(0)
data['Day'] = data['timestmp'].apply(lambda dt: dt.day)
data['TagNacht'] = data.apply(lambda x: tagnacht(x["timestampUNX"],x["sunrise"],x["sunset"]), axis = 1)

print(data)

dfs = []
for city in cities:
    dfs.append(data[ (data['ziel']==city) & (data['timestampUNX'] > (utc_today - 60*60*24*days)) ])
    #data['windspeed'] = (data['windspeed'].fillna(method='ffill')).rolling(10, min_periods=1).mean()


plt.figure(1)
plt.subplot(221)
for df in dfs:
    plt.plot(df['timestmp'],df['temperature'],linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Temperatur')
plt.title('Temperatur')

plt.subplot(222)
for df in dfs:
    plt.plot(df['timestmp'],df['temperaturegefuehlt'],linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Gefuehlte Temperatur')


plt.subplot(223)
for df in dfs:
    plt.plot(df['timestmp'],(df['humidity'].fillna(method='ffill')).rolling(10, min_periods=1).mean(),linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Luftfeuchtigkeit')


plt.subplot(224)
for df in dfs:
    plt.plot(df['timestmp'],(df['windspeed'].fillna(method='ffill')).rolling(10, min_periods=5).mean(),linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Windgeschwindigkeit')


sns.set_theme(style="ticks", palette="pastel")
plt.figure(2)

plt.subplot(1,2,1)
sns.boxplot(x="Day", y="temperature", hue = "ziel",
            data=data,
            linewidth=1, hue_order=cities)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("°C")
plt.title("Temperatur")
plt.grid(True)
plt.subplot(1,2,2)
sns.boxplot(x="Day", y="cloudiness", hue = "ziel",
            data=data[ data["TagNacht"] =="Tag" ],
            linewidth=1, hue_order=cities)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Bedeckungsgrad")
plt.title("Bewölkung")
plt.grid(True)

#print(plt.colormaps())
plt.show()