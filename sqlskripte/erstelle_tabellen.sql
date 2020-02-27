
CREATE TABLE Cities (
    ctyid INTEGER PRIMARY KEY,
    cityID TEXT NOT NULL,
    cityname TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    zeigeinvisu TEXT NOT NULL
);


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