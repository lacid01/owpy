import sqlite3
import weather
import pandas as pd
from datetime import datetime, timedelta
import sys


def execute(con,cursor,command):
    """
    Löst ein Kommando aus
    """
    cursor.execute(command)
    con.commit()

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


def getWetterTable(selectfilter = ""):
    """
    Gibt ein Array mit den Einträgen als Tupel wieder
    """
    sqlite_select_query = """SELECT * FROM Wetter ORDER BY country, city """

    records = getTableSelect(sqlite_select_query)
    return records

def showWettertabelle():
    tbl = getWetterTable()
    print("Einträge gesamt: %i" % len(tbl))
    for row in tbl:
        print(row)

def showWettertabelle2():
    tbl = getWetterTable()
    print("Einträge gesamt: %i" % len(tbl))
    for row in tbl:
        cty = getCity(row[16])[2]
        lokalerzeitstempel = (datetime.utcfromtimestamp(int(row[3]))+timedelta(hours=row[15]))
        print("%s, Stadt: %s -> %s, Zeitstempel: %s, Bescheibung: %s, Temperatur: %s°C, gefühlt: %s°C" % (row[1], row[2], cty, lokalerzeitstempel, row[7], row[9], row[10]) )

def getWettertableLetzteWerte(hide = "False"):
    if hide == "False":
        cityquery = """SELECT * FROM Cities ORDER BY cityname;"""
    else:
        cityquery = """SELECT * FROM Cities WHERE zeigeinvisu = '{}' ORDER BY cityname;""".format('True')
    cityrecords = getTableSelect(cityquery)

    cols = ['Land','Messort','Zielort','Beschreibung','Temperatur', 'Gefühlt', 'Zeitstempel', 'Zeitzone', 'Sonnenaufgang', 'Sonnenuntergang']
    df = pd.DataFrame(columns=cols)
    for cityrec in cityrecords:
        try:
            query = 'SELECT w.country, w.city, c.cityname as ziel, w.wthdescription, w.temperature,w.temperaturegefuehlt, w.timestmp, w.timezone, w.sunrise, w.sunset FROM Wetter as w INNER JOIN Cities as c ON c.ctyid = w.ctyid WHERE c.ctyid = {} ORDER BY w.timestmp DESC LIMIT 1'.format(cityrec[0])
            _df = pd.read_sql_query(query,sqlite3.connect('wetter.db'))

            _df['sunrise'] = _df.apply(lambda x : ((datetime.strptime(x['sunrise'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['timezone'])).strftime('%H:%M')), axis=1)
            _df['sunset'] = _df.apply(lambda x : ((datetime.strptime(x['sunset'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['timezone'])).strftime('%H:%M')), axis=1)
            _df.columns = cols
            _df['Zeitstempel'] = _df.apply(lambda x : ((datetime.strptime(x['Zeitstempel'], '%Y-%m-%d %H:%M:%S')+timedelta(hours=x['Zeitzone'])).strftime('%m.%d. %H:%M')), axis=1)

            df = df.append(_df,ignore_index=True)
        except Exception as e:
            print(e)
            pass
        
    #print(df)
    return df.sort_values(by=['Land','Zielort'])

def showWettertableLetzteWerte():
    wttrtable = getWettertableLetzteWerte()
    print(wttrtable.to_string(index=False))

def insertRow(wth):
    
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        
        sqlite_insert_query = """INSERT INTO Wetter
                            (country, city, timestampUNX, timestmp, sunrise, sunset, wthdescription, wthdescriptiondetailed, 
                            temperature, temperaturegefuehlt, humidity, pressure, windspeed, winddeg, timezone, ctyid) 
                            VALUES 
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        data_tuple = (
                    wth.country, 
                    wth.city, 
                    wth.timestampRAW,
                    wth.timestamp, 
                    wth.sunrise, 
                    wth.sunset, 
                    wth.description, 
                    wth.descriptiondetailed,
                    wth.temperature,
                    wth.temperaturegefuehlt,
                    wth.humidity,
                    wth.pressure,
                    wth.windspeed,
                    wth.winddeg,
                    wth.timezone,
                    wth.cityid
                    ) 

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        
        print("Record inserted successfully into Stoffstrom table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")
 
def addCity(alias,name,lat,lon,zeigeinvisu):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        
        sqlite_insert_query = """INSERT INTO Cities
                            (cityID, lat, lon, cityname, zeigeinvisu) 
                            VALUES 
                            (?,?,?,?,?)"""
        data_tuple = ( alias, lat, lon, name, zeigeinvisu ) 

        count = cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        
        print("Record inserted successfully into Cities table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")

def updateCityName(ctyid,name):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        print("UPDATE Cities SET name = '{}' WHERE cityID = '{}';".format(name,ctyid))

        count = cursor.execute("UPDATE Cities SET name = '{}' WHERE cityID = '{}';".format(name,ctyid))
        sqliteConnection.commit()
        
        print("Record inserted successfully into Cities table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")

def updateCityShowInVisu(ctyid,name):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        print("UPDATE Cities SET zeigeinvisu = '{}' WHERE cityID = '{}';".format(name,ctyid))

        count = cursor.execute("UPDATE Cities SET zeigeinvisu = '{}' WHERE cityID = '{}';".format(name,ctyid))
        sqliteConnection.commit()
        
        print("Record inserted successfully into Cities table ", cursor.rowcount)

        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")

def showCitiesRAW():
    try:

        query = 'SELECT * FROM Cities'
        sqldata = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['ctyid'])
        print(sqldata)
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)

def updateCity(alias,name,lat,lon,zeigeinvisu):
    query = 'SELECT * FROM Cities'
    dbid = pd.read_sql_query(query,sqlite3.connect('wetter.db')).set_index(['cityID']).loc[alias]['ctyid']

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


def showCities():
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        
        qlite_select_query = """SELECT * FROM Cities ORDER BY cityname;"""
        cursor.execute(qlite_select_query)

        records = cursor.fetchall()
        cursor.close()

        ctytable = pd.DataFrame.from_records(records).drop(0,axis = 1)
        ctytable.columns = ['ID','lat','lon','Name','Zeige in Visu']
        print(ctytable)
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def getCityTable():
    """
    Gibt ein DataFrame mit den Städten zurück
    """
    sqlite_select_query = """SELECT * FROM Cities ORDER BY ctyid"""

    records = getTableSelect(sqlite_select_query)
    ctytable = pd.DataFrame.from_records(records)
    ctytable.columns = ['FKID','ID','Name','lat','lon','Zeige in Visu']
    return ctytable


def getCity(cityid):
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        
        qlite_select_query = "SELECT * FROM Cities WHERE ctyid = {};".format(cityid)
        cursor.execute(qlite_select_query)

        records = cursor.fetchall()
        cursor.close()
        
        return records[0]
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def altertable():
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        with open('erstelle_tabellen.sql', 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        cursor.executescript(sql_script)
        print("SQLite script executed successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while executing sqlite script", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("sqlite connection is closed")

def create_timestamps_in_timestamptable():
    sqlite_select_query = """SELECT timestampUNX FROM Wetter ORDER BY timestampUNX LIMIT 1"""

    records = getTableSelect(sqlite_select_query)[0][0]
    print(datetime.utcfromtimestamp(int(records)))

    erster_zeitstempel_abgerundet = 1582804800
    letzter_zeitstempel_2020 = 1609453800

    zeitstempel_aktuell = 1582804800
    
    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        print("Start calculating timestamps...")
        data_tuple = []
        while zeitstempel_aktuell <= letzter_zeitstempel_2020:
            data_tuple.append((zeitstempel_aktuell,))
            zeitstempel_aktuell = zeitstempel_aktuell + 1800
            
        print("start with inserting...")
        sqlite_insert_query = """INSERT INTO Timestampsolver (timestampUNX) VALUES (?)"""
        count = cursor.executemany(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("Record inserted successfully into Stoffstrom table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("done...")