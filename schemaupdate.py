from typing import cast
import dbhelper as dbh
import sqlite3, json, requests
import pandas as pd


def increasedbversion():
    version = int(dbh.databaseversion())
    if version == 0:
        dbh.execCom("INSERT INTO databasesettings (key,value) VALUES ('Schema',{})".format(version+1))
    else:
        dbh.execCom("UPDATE databasesettings SET value = {} WHERE key = 'Schema'".format(version+1))


def runUpdate():
    currdbversion = dbh.databaseversion()
    if currdbversion <= 0:
        dbh.execCom("CREATE TABLE databasesettings (key TEXT NOT NULL, value INTEGER NOT NULL)")
        increasedbversion()

    if currdbversion <= 1:
        try:
            with open('sqlskripte/update1to2.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    
    if currdbversion <= 2:
        dbh.execCom("DELETE FROM databasesettings WHERE key = 'Schema'")
        dbh.execCom("INSERT INTO databasesettings (key,value) VALUES ('Schema',3)")

    if currdbversion < 4:
        try:
            with open('sqlskripte/update3to4.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 5:
        try:
            with open('sqlskripte/update4to5.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 6:
        try:
            with open('sqlskripte/update5to6.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
            
    if currdbversion < 7:
        try:
            with open('sqlskripte/update6to7.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)
            
    if currdbversion < 8:
        try:
            with open('sqlskripte/update7to8.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 9:
        try:
            with open('sqlskripte/update8to9.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 10:
        try:
            dbh.execCom("PRAGMA foreign_keys=OFF;")
            # Erstelle und Fuelle Laendertabelle und erstelle neue Citytable
            with open('sqlskripte/update9to10.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
            dbh.executeScript(sql_script)

            # Lade fuer jeden Eintrag in City JSON und Verknuepfe Codes 
            df = dbh.getCitiesDataFrame()
            _headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
            for index, row in df.iterrows():
                name = row['cityname']
                req = str(row['request'])
                print("Load json for {} with {}".format(name,req))
                _response = json.loads(requests.get(req, headers=_headers, verify = False).text)
                cntr = _response['sys']['country']
                print("Countrycode for {} is {}".format(name,cntr))
                cntrid = dbh.getTableSelect("SELECT id FROM Laendercodes WHERE ISO3166_alpha2 = '{}'".format(cntr))[0][0]
                print("id for Countrycode {} is {}".format(cntr,cntrid))
                dbh.execCom("UPDATE Cities SET countrylinkage = {} WHERE ctyid = '{}'".format(cntrid,index))
                #df = pd.read_sql_query("SELECT * FROM Cities WHERE cityname = '{}'".format(name),sqlite3.connect('wetter.db')).loc[0]

            print("Foreign Key ON")
            dbh.execCom("PRAGMA foreign_keys=ON;")
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 11:
        try:
            with open('sqlskripte/update10to11.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    if currdbversion < 12:
        try:
            with open('sqlskripte/update11to12.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    
    if currdbversion < 13:
        try:
            with open('sqlskripte/update12to13.sql', 'r') as sqlite_file:
                sql_script = sqlite_file.read()
                
            dbh.executeScript(sql_script)
            increasedbversion()
        except sqlite3.Error as error:
            print("Error while executing sqlite script", error)

    
    if currdbversion < 14:
        dbh.execCom("INSERT INTO databasesettings (key,value) VALUES ('TimeToNextLocationRequest',1500)")
        dbh.execCom("INSERT INTO databasesettings (key,value) VALUES ('TimeToNextLocationIteration',300000)")
        increasedbversion()

    if currdbversion < 15:
        dbh.execCom("INSERT INTO databasesettings (key,value) VALUES ('ConnectionTimeout',5)")
        increasedbversion()