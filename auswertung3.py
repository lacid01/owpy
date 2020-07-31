from matplotlib.pyplot import colormaps
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import sqlite3
import datetime as dt

cities = ['Naples','Gypsum','Grapevine','Owasso']
days = 3

query = "SELECT * FROM Wetter ORDER BY timestampUNX"

#data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
# lese sql
data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
# reduziere auf Abfragetage
utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
data = data[ data['timestampUNX'] > (utc_today - 60*60*24*days) ]
data['timestmp'] = data.apply(lambda x: dt.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=(60*60*x['timezone'])),axis=1) 

print(data)

dfs = []
for city in cities:
    dfs.append(data[ (data['city']==city) & (data['timestampUNX'] > (utc_today - 60*60*24*days)) ])


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
    plt.plot(df['timestmp'],df['humidity'],linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Luftfeuchtigkeit')


plt.subplot(224)
for df in dfs:
    plt.plot(df['timestmp'],df['windspeed'],linewidth=0.7)

plt.grid(True)
plt.legend(cities)
#plt.ylim([0,40])
plt.ylabel('Windgeschwindigkeit')
#print(plt.colormaps())
plt.show()