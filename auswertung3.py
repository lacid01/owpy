import pandas as pd
import sqlite3
from dbhelper import getTableSelect
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#%%
city = 'Michendorf'
days = 14
#%%

# Michendorf
# Vuollerim (SE) - Edefors
# Grundtjärn


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
        WHERE c.cityname = 'Michendorf' OR c.cityname = 'Schöneberg' ORDER BY w.timestampUNX"""

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
data['MonthDay'] = data['timestmp'].apply(lambda dt: dt.day)
data['Month'] = data['timestmp'].apply(lambda dt: mnth(dt.month))
data['Year'] = data['timestmp'].apply(lambda dt: dt.year)
data['Kat Wochentag'] = data['DayDt'].apply(lambda wd: we(wd))
data['Kat Jahreszeit'] = data['timestmp'].apply(lambda dt: jahreszeit(dt.month))
data['TagNacht'] = data.apply(lambda x: tagnacht(x["timestampUNX"],x["sunrise"],x["sunset"]), axis = 1)
print(data)



sns.relplot(
    data=data[ data["Kat Jahreszeit"] == "Winter" ], x="MonthDay", y="temperature", col="Month",
    hue="ziel", style="ziel", kind="line",
)

plt.show()