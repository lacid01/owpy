PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Cities_old;
DROP TABLE IF EXISTS Timestampsolver;

DROP TABLE IF EXISTS WetterActual;

CREATE TABLE WetterActual (
    country TEXT, 
    city TEXT, 
    descrid INTEGER, 
    temperature REAL,
    temperaturegefuehlt REAL, 
    timestmp TEXT, 
    timezone INT, 
    sunrise TEXT, 
    sunset TEXT,
    ctyid INTEGER
);

INSERT INTO WetterActual (
    country, 
    city, 
    descrid, 
    temperature,
    temperaturegefuehlt, 
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
    datetime(timestampUNX, 'unixepoch'), 
    timezone,
    datetime(sunrise, 'unixepoch'), 
    datetime(sunset, 'unixepoch'), 
    ctyid
  FROM Wetter ORDER BY timestampUNX DESC LIMIT 2
;

PRAGMA foreign_keys=ON;

VACUUM;