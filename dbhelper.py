import sqlite3
import weather
import pandas as pd
from datetime import datetime, timedelta


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
        cityquery = """SELECT * FROM Cities ORDER BY cityname WHERE zeigeinvisu = 'True';"""
    cityrecords = getTableSelect(cityquery)

    wttrlist = []
    for cityrec in cityrecords:
        
        try:
            row = getTableSelect("""SELECT * FROM Wetter WHERE ctyid = {} ORDER BY timestmp DESC LIMIT 1;""".format(cityrec[0]))[0]

            cty = getCity(row[16])[2]
            lokalerzeitstempel = (datetime.utcfromtimestamp(int(row[3]))+timedelta(hours=row[15]))
            wttrlist.append( (row[1], row[2], cty, row[7], row[9], row[10], lokalerzeitstempel ) )
            #print("%s, Stadt: %s -> %s, Zeitstempel: %s, Bescheibung: %s, Temperatur: %s°C, gefühlt: %s°C" % (row[1], row[2], cty, lokalerzeitstempel, row[7], row[9], row[10]) )
        except:
            pass

    try:
        wttrtable = pd.DataFrame.from_records(wttrlist)
        wttrtable.columns = ['Land','Messort','Stadt','Beschreibung','Temperatur', 'Gefühlt', 'Zeitstempel']
    except:
        wttrtable = pd.DataFrame()
    return wttrtable

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
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        
        qlite_select_query = """SELECT * FROM Cities;"""
        cursor.execute(qlite_select_query)

        records = cursor.fetchall()
        cursor.close()
        for rec in records:
            print(rec)
        
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


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
    Gibt ein Array mit den Einträgen als Tupel wieder
    """
    sqlite_select_query = """SELECT * FROM Cities ORDER BY ctyid"""

    records = getTableSelect(sqlite_select_query)
    return records


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