

ALTER TABLE log RENAME TO log_alt;

CREATE TABLE log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Timestamp TEXT, 
    Level TEXT,
    Message TEXT
);

INSERT INTO log 
(
    Timestamp,
    Level,
    Message
)
  SELECT 
    Timestamp,
    Level,
    Message
  FROM log_alt;

DROP TABLE IF EXISTS log_alt;


VACUUM;