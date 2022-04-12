import pandas as pd
import sqlite3
import datetime 
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from pandas.io.sql import DatabaseError
import seaborn as sns

#%%
cities = ['Michendorf','Beelitz','Bad Belzig','Schöneberg']
#%%

'''
def getquery(cty):
    return """SELECT  
        w.wetterid, c.cityname as ziel, w.timestampunx, datetime(w.timestampunx, 'unixepoch') AS timestmp, 
        cnd.condition, w.temperature,w.temperaturegefuehlt,w.humidity, w.timezone 
        FROM Wetter as w 
        INNER JOIN 
        (select ctyid as id, cityname FROM Cities) as c 
        ON c.id = w.ctyid 
        INNER JOIN
        (SELECT condition, condid FROM conditioncode) as cnd
        ON w.descrid = cnd.condid
        WHERE c.cityname = '""" + cty +"""' ORDER BY w.timestampUNX"""


print('Starte db-Abfrage...')
dtaMD = pd.read_sql_query(getquery('Michendorf'),sqlite3.connect('wetter2.db')).set_index(['wetterid'])
print('Starte Zeitstempelumrechnung...')
dtaMD['timestmp'] = dtaMD.apply(lambda x: datetime.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=(60*60*x['timezone'])),axis=1) 
cls = dtaMD.columns
cls2 = [ "md " + cls[cl] for cl in range(len(cls))]
dtaMD.columns = cls2
print(dtaMD)


print('Starte db-Abfrage...')
dtaSB = pd.read_sql_query(getquery('Schöneberg'),sqlite3.connect('wetter2.db')).set_index(['wetterid'])
print('Starte Zeitstempelumrechnung...')
dtaSB['timestmp'] = dtaSB.apply(lambda x: datetime.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=(60*60*x['timezone'])),axis=1) 
cls = dtaSB.columns
cls2 = [ "md " + cls[cl] for cl in range(len(cls))]
dtaSB.columns = cls2
print(dtaSB)

'''

###

query = """SELECT  
        w.wetterid, c.cityname as ziel, w.timestampunx, w.sunrise, w.sunset, datetime(w.timestampunx, 'unixepoch') AS timestmp, 
        cnd.condition, w.temperature,w.temperaturegefuehlt,w.humidity, w.cloudiness, w.timezone 
        FROM Wetter as w 
        INNER JOIN 
        (select ctyid as id, cityname FROM Cities) as c 
        ON c.id = w.ctyid 
        INNER JOIN
        (SELECT condition, condid FROM conditioncode) as cnd
        ON w.descrid = cnd.condid
        WHERE c.cityname = 'Bad Belzig' OR c.cityname = 'Michendorf' OR c.cityname = 'Schöneberg' ORDER BY w.timestampUNX"""

print('Starte db-Abfrage...')
data = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['wetterid'])
print('Starte Zeitstempelumrechnung...')
data['timestmp'] = data.apply(lambda x: datetime.datetime.strptime(x['timestmp'], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(seconds=(60*60*x['timezone'])),axis=1) 
print(data)


def we(wd):
    if wd >= 5:
        return "Weekend"
    else:
        return "Weekday"

def wkdy (wd):
    if wd == 0:
        return "Monday"
    if wd == 1:
        return "Tuesday"
    if wd == 2:
        return "Wednesday"
    if wd == 3:
        return "Thursday"
    if wd == 4:
        return "Friday"
    if wd == 5:
        return "Saturday"
    if wd == 6:
        return "Sunday"

def mnth (wd):
    if wd == 1:
        return "Jan"
    if wd == 2:
        return "Feb"
    if wd == 3:
        return "Mar"
    if wd == 4:
        return "Apr"
    if wd == 5:
        return "May"
    if wd == 6:
        return "June"
    if wd == 7:
        return "July"
    if wd == 8:
        return "Aug"
    if wd == 9:
        return "Sep"
    if wd == 10:
        return "Oct"
    if wd == 11:
        return "Nov"
    if wd == 12:
        return "Dec"

def jahreszeit (Monat):
    if (Monat > 2) and (Monat <= 5):
        return "Frühling"
    if Monat > 5 and Monat <= 8:
        return "Sommer"
    if Monat > 8 and Monat <= 11:
        return "Herbst"
    else:
        return "Winter"

def tagnacht(ts,tssunr,tssuns):
    if ts > tssunr and ts < tssuns:
        return "Tag"
    else:
        return "Nacht"


data['DayDt'] = data['timestmp'].apply(lambda dt : dt.weekday())
data['Day'] = data['DayDt'].apply(lambda wd: wkdy(wd))
data['Month'] = data['timestmp'].apply(lambda dt: mnth(dt.month))
data['Year'] = data['timestmp'].apply(lambda dt: dt.year)
data['Kat Wochentag'] = data['DayDt'].apply(lambda wd: we(wd))
data['Kat Jahreszeit'] = data['timestmp'].apply(lambda dt: jahreszeit(dt.month))
data['TagNacht'] = data.apply(lambda x: tagnacht(x["timestampUNX"],x["sunrise"],x["sunset"]), axis = 1)
print(data)

plt.figure()
plt.subplot(1,2,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Kat Jahreszeit", y="temperature", hue="Kat Wochentag",
            data=data[ data["ziel"] == "Schöneberg"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
ax = plt.gca()
ax.grid(True)


plt.figure(2)
plt.subplot(1,2,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Kat Jahreszeit", y="temperature", hue="TagNacht",
            data=data[ data["ziel"] == "Michendorf"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
ax = plt.gca()
ax.grid(True)


plt.subplot(1,2,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Kat Jahreszeit"] == "Sommer" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
ax = plt.gca()
ax.grid(True)



plt.figure(3)
plt.subplot(1,4,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "May" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
plt.title("Mai")
ax = plt.gca()
ax.grid(True)
plt.ylim([0,40])
plt.subplot(1,4,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "June" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("Juni")
ax = plt.gca()
ax.grid(True)
plt.ylim([0,40])
plt.subplot(1,4,3)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "July" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("Juli")
ax = plt.gca()
ax.grid(True)
plt.ylim([0,40])
plt.subplot(1,4,4)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "Aug" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("August")
ax = plt.gca()
ax.grid(True)
plt.ylim([0,40])



plt.figure(4)
plt.subplot(1,4,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "Jan" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
plt.title("Januar")
ax = plt.gca()
ax.grid(True)
plt.ylim([-15,25])
plt.subplot(1,4,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "Feb" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("Februar")
ax = plt.gca()
ax.grid(True)
plt.ylim([-15,25])
plt.subplot(1,4,3)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "Mar" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("März")
ax = plt.gca()
ax.grid(True)
plt.ylim([-15,25])
plt.subplot(1,4,4)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="TagNacht", y="temperature", hue="ziel",
            data=data[ data["Month"] == "Apr" ],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("")
plt.title("April")
ax = plt.gca()
ax.grid(True)
plt.ylim([-15,25])


plt.figure(5)

plt.subplot(1,2,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="temperature", hue="ziel",
            data=data,
            order=["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
plt.grid(True)


plt.subplot(1,2,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="temperaturegefuehlt", hue="ziel",
            data=data,
            order=["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Temperatur in °C")
ax2 = plt.gca()
ax2.grid(True)




plt.figure(6)
plt.subplot(1,2,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="cloudiness", hue="Kat Wochentag",
            data=data[ (data["ziel"] == "Michendorf") & (data["TagNacht"] == "Tag")],
            order=["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Bedeckungsgrad in %")
plt.grid(True)


plt.subplot(1,2,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="cloudiness", hue="TagNacht",
            data=data[ (data["ziel"] == "Michendorf")],
            order=["Jan","Feb","Mar","Apr","May","June","July","Aug","Sep","Oct","Nov","Dec"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Bedeckungsgrad in %")
plt.grid(True)



plt.figure(7)
plt.subplot(1,2,1)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="temperature", hue="Year",
            data=data[ (data["ziel"] == "Michendorf")],
            order=["Jan","Feb","Mar","Apr"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Bedeckungsgrad in %")
plt.grid(True)
plt.subplot(1,2,2)
sns.set_theme(style="ticks", palette="pastel")
sns.boxplot(x="Month", y="cloudiness", hue="TagNacht",
            data=data[ (data["ziel"] == "Michendorf")],
            order=["Jan","Feb","Mar","Apr"],
            linewidth=1)
sns.despine(offset=10)
#ax = sns.swarmplot(x="Day", y="Value", data=temperatur, color=".25", size=1)
plt.xlabel("")
plt.ylabel("Bedeckungsgrad in %")
plt.grid(True)

plt.show()
