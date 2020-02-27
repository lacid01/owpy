import sys,sqlite3

try:
    anlage = sys.argv[1]

    try:
        sqliteConnection = sqlite3.connect('wetter.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        with open('sqlskripte/' + sys.argv[1], 'r') as sqlite_file:
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

except Exception as e:
    print("Datei nicht gefunden.")
    print(e)