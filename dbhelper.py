import sqlite3

from pandas.io import sql
import weather
import pandas as pd
from datetime import datetime, timedelta
import sys
import requests, json, math

def execComFK(cmd):
    con = sqlite3.connect('wetter.db')
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys=1")
    con.commit()
    cursor.close()

    cursor = con.cursor()
    cursor.execute(cmd)
    con.commit()
    records = cursor.fetchall()
    cursor.close()
    return records

def executeScript(scrpt):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.executescript(scrpt)
        print("SQLite script executed successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)

def execCom(cmd):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        cursor.execute(cmd)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("execCom: Failed execute cmd: {}\nError: {}".format(cmd, error))
    return


def getTableSelect(select):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        
        cursor.execute(select)

        records = cursor.fetchall()
        cursor.close()

        return records
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("done...")


def listTables():
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        

        cursor.execute("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';""")

        records = cursor.fetchall()
        cursor.close()

        print(records)
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("done...")

def getWettertableLetzteWerte(hide = "False"):
    query = """
            SELECT 
            w.country, w.city, c.cityname || ' (' || w.country || ')'  as ziel, cd.condition, w.temperature,w.temperaturegefuehlt, w.humidity, hr.bezeichnerkurz, w.windspeed,
            w.timestmp as ts, w.timezone , w.sunrise, w.sunset
            FROM WetterActual as w 
            INNER JOIN 
            (SELECT * FROM Cities WHERE zeigeinvisu = 'True' ORDER BY cityname) as c 
            ON c.ctyid = w.ctyid
            INNER JOIN
            (SELECT * FROM conditioncode) as cd
            ON cd.condid = w.descrid
            INNER JOIN
            (SELECT * FROM Himmelsrichtung) as hr
            ON hr.richtungsid = 1 + CAST((w.winddirection + 11.25)/22.5 AS INTEGER)"""

    cols = ['Land','Messort','Zielort','Beschreibung','Temperatur', 'Gefühlt', 'Luftfeuchtigkeit', 'Windrichtung', 'ws', 'ts', 'utc', 'SoAu', 'SoUn']
    #df = pd.DataFrame(columns=cols)

    try:
        df = pd.read_sql_query(query,sqlite3.connect('wetter.db'))
        #print(df)
        df['sunrise'] = df.apply(lambda x : ((datetime.strptime(x['sunrise'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['timezone'])).strftime('%H:%M')), axis=1)
        df['sunset'] = df.apply(lambda x : ((datetime.strptime(x['sunset'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['timezone'])).strftime('%H:%M')), axis=1)
        df['ts'] = df.apply(lambda x : ((datetime.strptime(x['ts'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['timezone'])).strftime('%H:%M')), axis=1)
        df.columns = cols

        # Bisher keine gute Formel gefunden. Alles nur Nährungen
        def wbt(temperature, humidity):
            try:
                sum1 = temperature * math.atan(0.151977 * (humidity + 8.313659)**(1/2))
                sum2 = math.atan(temperature + humidity)
                sum3 = math.atan(humidity- 1.676331)
                sum4 = 0.00391838 *(humidity)**(3/2) * math.atan(0.023101 * humidity)
                _wbt = sum1 + sum2 - sum3 + sum4 - 4.686035
                return _wbt
            except:
                return 0
        df["FK Temp"] = df.apply(lambda x : "{0:.1f} °C".format(float(wbt(x['Temperatur'],x['Luftfeuchtigkeit']))), axis=1)

        #print(df)
        df['Temperatur'] = df['Temperatur'].apply(lambda x: "{0:.1f} °C".format(float(x)))
        df['Gefühlt'] = df['Gefühlt'].apply(lambda x: "{0:.1f} °C".format(float(x)))
        df['Windspeed'] = df['ws'].apply(lambda x: "{0:.1f} m/s".format(float(x)))
        #print(df)
        df = df[['Land','Messort','Zielort','Beschreibung','Temperatur', 'Gefühlt', 'FK Temp', 'Windrichtung', 'Windspeed', 'ts', 'utc', 'SoAu', 'SoUn']]
    except Exception as e:
        print(e)
        pass

    return df.sort_values(by=['Land','Zielort'])


def showWettertableLetzteWerte():
    wttrtable = getWettertableLetzteWerte()
    print(wttrtable.to_string(index=False))

def insertRow(wth):
    
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        #print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO Wetter
                                (country, city, timestampUNX, sunrise, sunset, descrid, 
                                temperature, temperaturemin, temperaturemax, temperaturegefuehlt, humidity, pressure, 
                                windspeed, winddeg, windgust, cloudiness, rain1h, snow1h, snow3h, timezone, ctyid) 
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data_tuple = (
                        wth.country, 
                        wth.city, 
                        wth.timestampRAW,
                        wth.sunrise, 
                        wth.sunset, 
                        wth.descrid,
                        wth.temperature,
                        wth.temperaturemin,
                        wth.temperaturemax,
                        wth.temperaturegefuehlt,
                        wth.humidity,
                        wth.pressure,
                        wth.windspeed,
                        wth.winddeg,
                        wth.windgust,
                        wth.cloudiness,
                        wth.rain,
                        wth.snow1h,
                        wth.snow3h,
                        wth.timezone,
                        wth.cityid
                        ) 

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        #print("{} inserted successfully into Wetter table {}".format(wth.city,cursor.rowcount))

        #print("Record deleted successfully from WetterActual table ", cursor.rowcount)
        cursor.close()
        updateWetterActual(wth)

    except sqlite3.Error as error:
        print("Error while inserted into Wetter table City {}, Error: {}".format(wth.city,error))
    '''finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")'''

def updateWetterActual(wth):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()

        qury = "DELETE FROM WetterActual WHERE ctyid = {};".format(wth.cityid)
        cursor.execute(qury)
        sqliteConnection.commit()

        sqlite_insert_query = """INSERT OR REPLACE INTO WetterActual
                                (country, city, descrid, temperature,temperaturegefuehlt,
                                humidity, winddirection, windspeed, timestmp, timezone, sunrise, sunset, ctyid) 
                                VALUES 
                                (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data_tuple = (
                        wth.country, 
                        wth.city, 
                        wth.descrid,
                        wth.temperature,
                        wth.temperaturegefuehlt,
                        wth.humidity,
                        wth.winddeg,
                        wth.windspeed,
                        wth.timestamp, 
                        wth.timezone,
                        datetime.utcfromtimestamp(wth.sunrise), 
                        datetime.utcfromtimestamp(wth.sunset), 
                        wth.cityid
                        ) 

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        #print("{} inserted successfully into WetterActual table {}".format(wth.city,cursor.rowcount))
        cursor.close()
    except sqlite3.Error as error:
        print("Error while inserted into WetterActual table City {}, Error: {}".format(wth.city,error))


def addCity(name,lat,lon,zeigeinvisu):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = """INSERT INTO Cities
                            (lat, lon, cityname, zeigeinvisu, active) 
                            VALUES 
                            (?,?,?,?,1)"""
        data_tuple = ( lat, lon, name, zeigeinvisu ) 
        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()        
        cursor.close()

        updaterequ = '''UPDATE Cities SET 
            request = 'http://api.openweathermap.org/data/2.5/weather?lat=' || lat || '&lon=' || lon || '&appid=53dafd10eab9188765711009650ab647'
            WHERE request ISNULL'''
        execCom(updaterequ)

        # Local Zeitstempel wann added bzw. erste Werte und Land
        df = pd.read_sql_query("SELECT * FROM Cities WHERE cityname = '{}'".format(name),sqlite3.connect('wetter.db')).loc[0]
        _headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
        _response = json.loads(requests.get(str(df['request']), headers=_headers, verify = False).text)
        locts = _response['timezone'] + _response['dt']
        cntrid = countryid(_response['sys']['country'])
        execCom("UPDATE Cities SET firstadded = {}, countrylinkage = {} WHERE cityname = '{}'".format(locts,cntrid,name))

        print("Record inserted successfully into Cities table ", cursor.rowcount)


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")

def updateCitiesAddedDate():
    req = '''UPDATE Cities 
        SET 
        firstadded = 
            (
                SELECT tbl.firstval FROM
                    (SELECT c.ctyid,MIN(w.ts) as firstval FROM Cities c
                    INNER JOIN 
                    (SELECT timestampUNX+timezone*3600 as ts, ctyid FROM Wetter) w
                    ON w.ctyid = c.ctyid
                    GROUP BY c.ctyid) tbl
                WHERE Cities.ctyid = tbl.ctyid
            )'''
    execCom(req)
    Log("Cities updated successfully")

def updateCityName(ctyid,name):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        print("UPDATE Cities SET name = '{}' WHERE ctyid = '{}';".format(name,ctyid))

        count = cursor.execute("UPDATE Cities SET name = '{}' WHERE ctyid = '{}';".format(name,ctyid))
        sqliteConnection.commit()
        
        print("Record inserted successfully into Cities table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")

def ShowInVisuSwitch(ctyid):
    try:
        query = "SELECT zeigeinvisu FROM Cities WHERE ctyid = {};".format(ctyid)
        IsInVisu = execComFK(query)[0][0]
        if IsInVisu == 'True':
            print("Switch to False")
            query2 = "UPDATE Cities SET zeigeinvisu = 'False' WHERE ctyid = {};".format(ctyid)
            execComFK(query2)
        else:
            print("Switch to True")
            query2 = "UPDATE Cities SET zeigeinvisu = 'True' WHERE ctyid = {};".format(ctyid)
            execComFK(query2)

        query = "SELECT zeigeinvisu FROM Cities WHERE ctyid = {};".format(ctyid)
        IsInVisu = execComFK(query)[0][0]
        print("new Value = {}".format(IsInVisu))

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

def getCitiesDataFrame():
    try:

        query = '''SELECT *, datetime(firstadded, 'unixepoch') AS added FROM Cities'''
        sqldata = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['ctyid'])
        return sqldata        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)

def showCitiesRAW():
    try:
        sqldata = getCitiesDataFrame()
        pd.set_option('display.max_rows', 500)
        print(sqldata.sort_values(by=['cityname']))        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)



def updateCity(name,lat,lon,zeigeinvisu):
    query = 'SELECT * FROM Cities'
    dbid = getTableSelect("SELECT ctyid FROM Cities WHERE cityname = '{}'".format(name))[0][0]

    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        print("UPDATE Cities SET cityname = '{}',lat = '{}',lon='{}',zeigeinvisu = '{}' WHERE ctyid = '{}';".format(name,lat,lon,zeigeinvisu,dbid))

        count = cursor.execute("UPDATE Cities SET cityname = '{}',lat = '{}',lon='{}',zeigeinvisu = '{}' WHERE ctyid = '{}';".format(name,lat,lon,zeigeinvisu,dbid))
        sqliteConnection.commit()
        
        print("Record inserted successfully into Cities table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)


def getCityTable():
    """
    Gibt ein DataFrame mit den Städten zurück
    """
    sqlite_select_query = """SELECT ctyid, cityname, lat, lon, zeigeinvisu, firstadded, request FROM Cities ORDER BY ctyid"""

    records = getTableSelect(sqlite_select_query)
    ctytable = pd.DataFrame.from_records(records)
    ctytable.columns = ['FKID','Name','lat','lon','Zeige in Visu','added','request']
    return ctytable

def getCityTableLike(pattern):
    """
    Gibt ein DataFrame mit den Städten zurück
    """
    sqlite_select_query = """SELECT * FROM Cities WHERE cityname LIKE '%{}%' ORDER BY ctyid""".format(pattern)

    records = getTableSelect(sqlite_select_query)
    ctytable = pd.DataFrame.from_records(records)
    return ctytable


def getCity(cityid):
    try:
        qlite_select_query = "SELECT * FROM Cities WHERE ctyid = {};".format(cityid)
        records = execComFK(qlite_select_query)
        return records[0]
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)

def deleteCityById(cityid):
    try:
        qlite_select_query = "DELETE FROM Cities WHERE ctyid = {};".format(cityid)
        execComFK(qlite_select_query)
        return
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

def deleteCityByName(name):
    try:
        qlite_select_query = "DELETE FROM Cities WHERE cityname = '{}';".format(name)
        execComFK(qlite_select_query)
        return
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

def settings(Key):
    try:
        qlite_select_query = "SELECT value FROM databasesettings WHERE key = '{}'".format(Key)
        records = execComFK(qlite_select_query)    
        return records[0][0]    
    except sqlite3.Error as error:
        print("Failed to read data from databasesettings", error)
        return 0


def settingsUpdate(Key,Value):
    try:
        qlite_select_query = "UPDATE databasesettings SET value = {} WHERE key = '{}'".format(Value,Key)
        execCom(qlite_select_query)
    except sqlite3.Error as error:
        print("Failed to write data to databasesettings", error)
        return 0

def databaseversion():
    return settings('Schema')

def databaseversionDecrease():
    version = databaseversion()
    try:
        qlite_select_query = "UPDATE databasesettings SET value = {} WHERE key = 'Schema'".format(version-1)
        execCom(qlite_select_query)
    except sqlite3.Error as error:
        print("Failed to read data from databasesettings", error)
        return 0
    print("Old db Version: {}, new db Version: {}".format(version,databaseversion()))
   
def Log(message, level = "Info"):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO log (Timestamp, Level, Message) VALUES (?,?,?);"""
        data_tuple = (datetime.now(), level, message) 

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        cursor.close()
    except Exception as error:
        print("Failed to write in log table", error)

def LogRead(Level = '', Limit = 10, Order = 'DESC'):
    Filter = ''
    if len(Level) > 0:
        Filter = """WHERE Level = '""" + Level + """'"""

    query = """SELECT * FROM log {} ORDER BY id {} LIMIT {}""".format(Filter,Order,Limit)
    df = pd.read_sql_query(query,sqlite3.connect('wetter.db'))
    #print(df)
    #print(df.columns.tolist())
    return df

def LogToCsv(Path = 'LogExport.csv', Level = '', Order = 'DESC'):
    LogRead(Limit=10000, Order = Order, Level = Level).to_csv(Path,sep=';',index=True)

def countryid(country):
    try:
        cntrid = getTableSelect("SELECT id FROM Laendercodes WHERE ISO3166_alpha2 = '{}'".format(country))[0][0]
        return cntrid
    except sqlite3.Error as error:
        print("Failed to read from Laendercodes table", error)

def updateCitytableCountryId():
    df = getCitiesDataFrame()
    _headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
    for index, row in df.iterrows():
        name = row['cityname']
        print("Start for {}...".format(name))
        ctyid = index
        req = str(row['request'])
        print("Load json for {} ({}) with {}".format(name,ctyid,req))
        _response = json.loads(requests.get(req, headers=_headers, verify = False).text)
        cntr = _response['sys']['country']
        print("Countrycode for {} is {}".format(name,cntr))
        cntrid = getTableSelect("SELECT id FROM Laendercodes WHERE ISO3166_alpha2 = '{}'".format(cntr))[0][0]
        print("id for Countrycode {} is {}".format(cntr,cntrid))
        execCom("UPDATE Cities SET countrylinkage = {} WHERE ctyid = '{}'".format(cntrid,ctyid))