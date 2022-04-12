import pandas as pd
import sqlite3
from dbhelper import getTableSelect
import datetime as dt
import matplotlib.pyplot as plt
import time

#%%
cities = 'Michendorf'
cities = 'Berlin Schoeneberg'
days = 1200


utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
younger_than = (utc_today - 60*60*24*days)

query = "SELECT *, datetime(timestampunx, 'unixepoch') AS timestmp, datetime(sunrise, 'unixepoch', 'utc') AS sunrisedt, datetime(sunset, 'unixepoch', 'utc') AS sunsetdt FROM Wetter as w INNER JOIN (select ctyid as id, cityname FROM Cities) as c ON c.id = w.ctyid WHERE w.city = '" + cities + "' AND CAST(w.timestampunx AS INTEGER) > CAST(" + str(younger_than) + " AS INTEGER) ORDER BY w.timestampUNX"
#query = "SELECT * FROM Wetter w WHERE w.ctyid = (SELECT ctyid FROM Cities WHERE cityname = '"  + cities + "') AND CAST(w.timestampunx AS INTEGER) > CAST(" + str(younger_than) + " AS INTEGER) ORDER BY w.timestampUNX"

#data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
print(query)
print('Starte db-Abfrage...')
now = time.time()
data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid'])
duration = time.time() - now
print("Abfrage fertig in " + str(duration) + "s")

data['rain1h'] = data['rain1h'].fillna(0)
data['cloudiness'] = data['cloudiness'].apply( lambda x: x/100.)
data['humidity'] = data['humidity'].apply( lambda x: x/100.)
data['timestmp'] = data.apply(lambda x: dt.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=(60*60*x['timezone'])),axis=1) 
data['daylength'] = data.apply(lambda x: int((dt.datetime.strptime(x['sunsetdt'], '%Y-%m-%d %H:%M:%S') - dt.datetime(1970,1,1)).total_seconds()) - int((dt.datetime.strptime(x['sunrisedt'], '%Y-%m-%d %H:%M:%S') - dt.datetime(1970,1,1)).total_seconds()), axis=1 )
data['rain1hcumsum'] = data['rain1h'].cumsum()

data = data.drop(columns=['timestampUNX','country','city','timezone','id','ctyid'])

print(data)
print(data.columns)
#print(data[data.columns])
dta = data[['cityname','timestmp','temperature','humidity','windspeed','winddeg','cloudiness','daylength']]
dta.to_csv('data.csv', sep=';', decimal=',')