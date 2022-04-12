PRAGMA foreign_keys=OFF;

ALTER TABLE Cities RENAME TO Cities_old;

CREATE TABLE Cities (
    ctyid INTEGER PRIMARY KEY,
    cityname TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    zeigeinvisu TEXT NOT NULL,
    firstadded INTEGER,
    request TEXT
);

INSERT INTO Cities (
    ctyid, 
    cityname, 
    lat, 
    lon,
    zeigeinvisu,
    firstadded
) 
SELECT 
    ctyid, 
    cityname, 
    lat, 
    lon,
    zeigeinvisu,
    firstadded
  FROM Cities_old
;

DROP TABLE IF EXISTS Cities_old;

PRAGMA foreign_keys=ON;

UPDATE 
    Cities
SET 
    request = "http://api.openweathermap.org/data/2.5/weather?lat=" || lat || "&lon=" || lon || "&appid=53dafd10eab9188765711009650ab647";

VACUUM;