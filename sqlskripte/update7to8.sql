UPDATE Cities 
SET 
firstadded = 
    (
        SELECT tbl.firstval FROM
            (SELECT c.ctyid,MIN(w.ts) as firstval FROM Cities c
            INNER JOIN 
            (SELECT timestampUNX+timezone*3600 as ts, ctyid FROM Wetter) w
            ON w.ctyid = c.ctyid
            GROUP BY c.ctyid) tbl
        WHERE Cities.ctyid = tbl.ctyid
    );