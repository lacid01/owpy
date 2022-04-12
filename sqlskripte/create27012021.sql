
DROP TABLE IF EXISTS WetterActual;
CREATE TABLE WetterActual (
    country TEXT, 
    city TEXT, 
    wthdescription TEXT, 
    temperature REAL,
    temperaturegefuehlt REAL, 
    timestmp TEXT, 
    timezone INT, 
    sunrise TEXT, 
    sunset TEXT,
    ctyid INTEGER
)