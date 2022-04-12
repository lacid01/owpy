
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Wetter_old;

ALTER TABLE Wetter RENAME TO Wetter_old;

CREATE TABLE Wetter (
    wetterid INTEGER PRIMARY KEY,
    country TEXT,
    city TEXT NOT NULL,
    timestampUNX INTEGER NOT NULL,
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
    rain1h REAL,
    timezone INTEGER,
    ctyid INTEGER,
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid)
);

INSERT INTO Wetter (wetterid, country, city, timestampUNX, timestmp, sunrise,sunset,wthdescription,wthdescriptiondetailed,temperature,temperaturegefuehlt,humidity,pressure,windspeed,winddeg,timezone,ctyid)
  SELECT wetterid, country, city, timestampUNX, timestmp, sunrise,sunset,wthdescription,wthdescriptiondetailed,temperature,temperaturegefuehlt,humidity,pressure,windspeed,winddeg,timezone,ctyid
  FROM Wetter_old;



DROP TABLE IF EXISTS Wetter_old;

PRAGMA foreign_keys=ON;

VACUUM;