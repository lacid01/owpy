import pandas as pd
from dbhelper import getTableSelect
from matplotlib.pyplot import *

rec = getTableSelect("SELECT w1.timestmp,w1.city,w1.temperature,w2.timestmp,w2.city,w2.temperature,w1.temperature - w2.temperature as diff FROM Wetter w1,Wetter w2 WHERE w1.ctyid <> w2.ctyid AND ABS(w1.timestampUNX - w2.timestampUNX) < 300 AND w1.city LIKE ('%Mich%') AND w2.city LIKE ('%Schoe%') ORDER BY w1.timestampUNX")
data = pd.DataFrame.from_records(rec)
data.columns = ['ts Mich', 'c1', 'tmich', 'ts Schoe', 'c2', 'tsb', 'tdiff']

figure(1)
subplot(211)
plot(data['ts Mich'],data['tdiff'],color='blue', linewidth=1.0, snap=True)

subplot(212)
plot(data['ts Mich'],data['tmich'],color='blue', linewidth=1.0, snap=True)
plot(data['ts Mich'],data['tsb'],color='red', linewidth=1.0, snap=True)
show()