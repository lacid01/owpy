
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Wetter_old;

ALTER TABLE Wetter RENAME TO Wetter_old;

CREATE TABLE Wetter (
    wetterid INTEGER PRIMARY KEY,
    country TEXT,
    city TEXT NOT NULL,
    timestampUNX INTEGER NOT NULL,
    sunrise INTEGER,
    sunset INTEGER,
    wthdescription TEXT,
    wthdescriptiondetailed TEXT,
    temperature REAL,
    temperaturemin REAL,
    temperaturemax REAL,
    temperaturegefuehlt REAL,
    humidity INTEGER,
    pressure INTEGER,
    windspeed REAL,
    winddeg INTEGER,
    windgust REAL,
    cloudiness INTEGER,
    rain1h REAL,
    snow1h REAL,
    snow3h REAL,
    timezone INTEGER,
    ctyid INTEGER,
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid)
);

INSERT INTO Wetter 
(
    wetterid,
    country,
    city,
    timestampUNX,
    sunrise,
    sunset,
    wthdescription,
    wthdescriptiondetailed,
    temperature,
    temperaturemin,
    temperaturemax,
    temperaturegefuehlt,
    humidity,
    pressure,
    windspeed,
    winddeg,
    windgust,
    cloudiness,
    rain1h,
    snow1h,
    snow3h,
    timezone,
    ctyid
)
  SELECT 
    wetterid, 
    country, 
    city, 
    timestampUNX, 
    CAST(strftime('%s', sunrise) AS INT),
    CAST(strftime('%s', sunset) AS INT),
    wthdescription,
    wthdescriptiondetailed,
    temperature,
    temperaturemin,
    temperaturemax,
    temperaturegefuehlt,
    humidity,
    pressure,
    windspeed,
    winddeg,
    windgust,
    cloudiness,
    rain1h,
    snow1h,
    snow3h,
    timezone,
    ctyid
  FROM Wetter_old;



DROP TABLE IF EXISTS Wetter_old;

PRAGMA foreign_keys=ON;

VACUUM;