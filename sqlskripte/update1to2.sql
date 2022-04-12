PRAGMA foreign_keys=OFF;

ALTER TABLE WetterActual RENAME TO WetterActual_old;

CREATE TABLE WetterActual (
    country TEXT, 
    city TEXT, 
    descrid INTEGER, 
    temperature REAL,
    temperaturegefuehlt REAL, 
    winddirection INTEGER, 
    windspeed INTEGER, 
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
    winddirection, 
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
    winddirection, 
    timestmp, 
    timezone, 
    sunrise, 
    sunset,
    ctyid
  FROM WetterActual_old
;

DROP TABLE IF EXISTS WetterActual_old;

PRAGMA foreign_keys=ON;

VACUUM;