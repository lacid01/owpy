PRAGMA foreign_keys=OFF;

ALTER TABLE Cities RENAME TO Cities_old;

CREATE TABLE Cities (
    ctyid INTEGER PRIMARY KEY,
    cityname TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    zeigeinvisu TEXT NOT NULL,
    added INTEGER
);

INSERT INTO Cities (
    ctyid, 
    cityname, 
    lat, 
    lon,
    zeigeinvisu
) 
SELECT 
    ctyid, 
    cityname, 
    lat, 
    lon,
    zeigeinvisu
  FROM Cities_old
;

DROP TABLE IF EXISTS Cities_old;

PRAGMA foreign_keys=ON;

VACUUM;