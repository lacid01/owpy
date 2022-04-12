
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
    FOREIGN KEY (ctyid) REFERENCES Cities (ctyid),
    FOREIGN KEY (descrid) REFERENCES conditioncode (condid)
);

INSERT INTO Wetter 
(
    wetterid,
    country, city,
    timestampUNX, sunrise, sunset,
    descrid,
    temperature, temperaturemin, temperaturemax, temperaturegefuehlt,
    humidity, pressure, windspeed, winddeg, windgust,
    cloudiness, rain1h, snow1h, snow3h,
    timezone, ctyid
)
  SELECT 
    wo.wetterid, 
    wo.country, 
    wo.city, 
    wo.timestampUNX, 
    wo.sunrise,
    wo.sunset,
    cond.condid,
    wo.temperature,
    wo.temperaturemin,
    wo.temperaturemax,
    wo.temperaturegefuehlt,
    wo.humidity,
    wo.pressure,
    wo.windspeed,
    wo.winddeg,
    wo.windgust,
    wo.cloudiness,
    wo.rain1h,
    wo.snow1h,
    wo.snow3h,
    wo.timezone,
    wo.ctyid
  FROM Wetter_old AS wo LEFT JOIN conditioncode as cond ON cond.descr = wo.wthdescriptiondetailed;



DROP TABLE IF EXISTS Wetter_old;

PRAGMA foreign_keys=ON;

VACUUM;