import pandas as pd
import sqlite3
from dbhelper import getTableSelect
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns


#%%
city = 'Longyearbyen' #'Longyearbyen'
days = 14
#%%

# Michendorf
# Vuollerim (SE) - Edefors
# Grundtjärn
# Kolympia, Rhodos

utc_today = int((dt.datetime.today() - dt.datetime(1970,1,1)).total_seconds())
younger_than = (utc_today - 60*60*24*days)



#query = "SELECT * FROM Wetter as w INNER JOIN Cities as c ON c.ctyid = w.ctyid WHERE w.city = '"  + city + "' AND CAST(w.timestampunx AS INTEGER) > CAST(" + str(younger_than) + " AS INTEGER) ORDER BY w.timestampUNX"
query = "SELECT *, datetime(timestampunx, 'unixepoch') AS timestmp FROM Wetter w WHERE w.ctyid = (SELECT ctyid FROM Cities WHERE cityname = '"  + city + "') AND CAST(w.timestampunx AS INTEGER) > CAST(" + str(younger_than) + " AS INTEGER) ORDER BY w.timestampUNX"
print('Starte db-Abfrage...')
data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid','country'])
print(str(data.size) + "/10 Daten abgefragt")


print('Starte Zeitstempelumrechnung...')
data['timestmp'] = data.apply(lambda x: dt.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + dt.timedelta(seconds=(60*60*x['timezone'])),axis=1) 

print(data)
#print(data.dtypes)
#print(data.columns)
#print(data['temperaturemin'])


def tagnacht(ts,tssunr,tssuns):
    if ts > tssunr and ts < tssuns:
        return "Tag"
    else:
        return "Nacht"

data['windspeed'] = (data['windspeed'].fillna(method='ffill')).rolling(10, min_periods=1).mean()
data['windgust'] = (data['windgust'].fillna(method='ffill')).rolling(10, min_periods=1).mean()
data['rain1h'] = data['rain1h'].fillna(0)
data['Day'] = data['timestmp'].apply(lambda dt: dt.day)
data['TagNacht'] = data.apply(lambda x: tagnacht(x["timestampUNX"],x["sunrise"],x["sunset"]), axis = 1)


plt.figure(1)
plt.subplot(221)
plt.plot(data['timestmp'],data['temperature'],'black',linewidth=0.7)
plt.plot(data['timestmp'],data['temperaturemin'],'blue',linewidth=0.7)
plt.plot(data['timestmp'],data['temperaturemax'],'red',linewidth=0.7)
plt.grid(True)
plt.legend(['Temperatur','Temperatur Min','Temperatur Max'])
#plt.ylim([0,40])
plt.ylabel('Temperatur')
plt.title('Temperatur')



plt.subplot(222)
plt.plot(data['timestmp'],data['humidity'],'blue',linewidth=0.7)
plt.plot(data['timestmp'],data['cloudiness'],'grey', linewidth=0.7)

plt.grid(True)
plt.legend(['Luftfeuchtigkeit','Bedeckungsgrad'])
#plt.ylim([0,40])
plt.ylabel('%')


plt.subplot(223)
plt.plot(data['timestmp'],data['windspeed'],linewidth=0.7)
plt.plot(data['timestmp'],data['windgust'],'grey',linewidth=0.7)

plt.grid(True)
plt.legend(['Geschwindigkeit','Böen'])
#plt.ylim([0,40])
plt.ylabel('Windgeschwindigkeit in m/s')


plt.subplot(224)
plt.plot(data['timestmp'],data['rain1h'],linestyle="dotted")

plt.grid(True)
plt.legend(['Niederschlag'])
#plt.ylim([0,40])
plt.ylabel('mm')

#plt.figure(2)
#plt.plot(data['timestmp'],data.apply(lambda x: int((dt.datetime.strptime(x['sunset'], '%Y-%m-%d %H:%M:%S') - dt.datetime(1970,1,1)).total_seconds()) - int((dt.datetime.strptime(x['sunrise'], '%Y-%m-%d %H:%M:%S') - dt.datetime(1970,1,1)).total_seconds()), axis=1 ))

#print(plt.colormaps())

sns.set_theme(style="ticks", palette="pastel")
try:
    plt.figure(2)
    plt.subplot(1,2,1)
    sns.boxplot(x="Day", y="temperature",  hue="TagNacht",
                data=data,
                linewidth=1)
    sns.despine(offset=10)
    #ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
    plt.xlabel("")
    plt.ylabel("Temperatur in °C")
    plt.title("Temperatur")
    plt.grid(True)

    plt.subplot(1,2,2)
    sns.boxplot(x="Day", y="cloudiness",
                data=data[ data["TagNacht"] =="Tag" ],
                linewidth=1)
    sns.despine(offset=10)
    #ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
    plt.xlabel("")
    plt.ylabel("Bedeckungsgrad")
    plt.title("Bewölkung")
    plt.grid(True)

    sns.relplot(
        data=data, x="Day", y="temperature", kind="line",hue="TagNacht"
    )
    plt.grid(True)
except:
    pass

plt.show()