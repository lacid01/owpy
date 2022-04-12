PRAGMA foreign_keys=OFF;

ALTER TABLE Wetter RENAME TO Wetter_old;

CREATE TABLE Wetter (
    wetterid INTEGER PRIMARY KEY,
    country TEXT,
    city TEXT NOT NULL,
    timestampUNX INTEGER NOT NULL,
    sunrise INTEGER,
    sunset INTEGER,
    descrid INTEGER,
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
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid) ON DELETE CASCADE,
    FOREIGN KEY (descrid) REFERENCES conditioncode (condid) ON DELETE SET NULL
);

INSERT INTO Wetter 
    (wetterid,
    country,
    city,
    timestampUNX,
    sunrise,
    sunset,
    descrid,
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
    ctyid)
SELECT 
    wetterid,
    country,
    city,
    timestampUNX,
    sunrise,
    sunset,
    descrid,
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


ALTER TABLE Cities RENAME TO Cities_old;
CREATE TABLE Cities (
    ctyid INTEGER PRIMARY KEY,
    cityname TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    zeigeinvisu TEXT NOT NULL,
    firstadded INTEGER,
    request TEXT,
    active INTEGER NOT NULL,
    countrylinkage INTEGER,
    FOREIGN KEY (countrylinkage) REFERENCES Laendercodes (id) ON DELETE SET NULL
);

INSERT INTO Cities (
    ctyid,
    cityname,
    lat,
    lon,
    zeigeinvisu,
    firstadded,
    request,
    active,
    countrylinkage
)
SELECT
    ctyid,
    cityname,
    lat,
    lon,
    zeigeinvisu,
    firstadded,
    request,
    active,
    countrylinkage
FROM Cities_old;

ALTER TABLE WetterActual RENAME TO WetterActual_old;
CREATE TABLE WetterActual (
    country TEXT, 
    city TEXT, 
    descrid INTEGER, 
    temperature REAL,
    temperaturegefuehlt REAL, 
    humidity INTEGER, 
    winddirection INTEGER, 
    windspeed INTEGER, 
    timestmp TEXT, 
    timezone INT, 
    sunrise TEXT, 
    sunset TEXT,
    ctyid INTEGER,
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid) ON DELETE CASCADE
);

INSERT INTO WetterActual (
    country, 
    city, 
    descrid, 
    temperature,
    temperaturegefuehlt, 
    humidity, 
    winddirection, 
    windspeed, 
    timestmp, 
    timezone, 
    sunrise, 
    sunset,
    ctyid
)
SELECT
    country, 
    city, 
    descrid, 
    temperature,
    temperaturegefuehlt, 
    humidity, 
    winddirection, 
    windspeed, 
    timestmp, 
    timezone, 
    sunrise, 
    sunset,
    ctyid
FROM WetterActual_old;

DROP TABLE Wetter_old;
DROP TABLE WetterActual_old;
DROP TABLE Cities_old;

VACUUM;