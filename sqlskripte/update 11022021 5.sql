PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS Himmelsrichtung;

CREATE TABLE Himmelsrichtung (
    richtungsid INTEGER PRIMARY KEY,
    bezeichnerkurz TEXT, 
    bezeichnerlang TEXT
);

INSERT INTO Himmelsrichtung (
    richtungsid, 
    bezeichnerkurz, 
    bezeichnerlang
) 
VALUES
(1,'N','Nord'),
(2,'NNO','Nord Nord Ost'),
(3,'NO','Nord Ost'),
(4,'ONO','Ost Nord Ost'),
(5,'O','Ost'),
(6,'OSO','Ost Süd Ost'),
(7,'SO','Süd Ost'),
(8,'SSO','Süd Süd Ost'),
(9,'S','Süd'),
(10,'SSW','Süd Süd West'),
(11,'SW','Süd West'),
(12,'WSW','West Süd West'),
(13,'W','West'),
(14,'WNW','West Nord West'),
(15,'NW','Nord West'),
(16,'NNW','Nord Nord West'),
(17,'N','Nord')
;

ALTER TABLE WetterActual RENAME TO WetterActual_old;

CREATE TABLE WetterActual (
    country TEXT, 
    city TEXT, 
    descrid INTEGER, 
    temperature REAL,
    temperaturegefuehlt REAL, 
    winddirection INTEGER, 
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