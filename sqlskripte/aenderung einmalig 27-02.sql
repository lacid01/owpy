DROP TABLE IF EXISTS Wetter;
DROP TABLE IF EXISTS Cities_old_2;
DROP TABLE IF EXISTS Cities;


CREATE TABLE Cities (
    ctyid INTEGER PRIMARY KEY,
    cityID TEXT NOT NULL,
    cityname TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    zeigeinvisu TEXT NOT NULL
);

INSERT INTO Cities (cityID, cityname, lat, lon, zeigeinvisu)
  SELECT cityID, name, lat, lon, zeigeinvisu
  FROM Cities_old;

CREATE TABLE Wetter (
    wetterid INTEGER PRIMARY KEY,
    country TEXT,
    city TEXT NOT NULL,
    timestampUNX TEXT NOT NULL,
    timestmp TEXT NOT NULL,
    sunrise TEXT,
    sunset TEXT,
    wthdescription TEXT,
    wthdescriptiondetailed TEXT,
    temperature REAL,
    temperaturegefuehlt REAL,
    humidity INTEGER,
    pressure INTEGER,
    windspeed REAL,
    winddeg INTEGER,
    timezone INTEGER,
    ctyid INTEGER,
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid)
);