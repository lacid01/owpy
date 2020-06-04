import pandas as pd
from dbhelper import getTableSelect
from matplotlib.pyplot import *

print('Read database...')
#rec = getTableSelect("SELECT w.timestmp,w.timestampUNX,w.city,w.temperature,w.timestampUNX-tss.timestampUNX FROM Wetter w,Timestampsolver tss WHERE ABS(w.timestampUNX - tss.timestampUNX) < 900 AND (w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%') OR w.city LIKE ('%Belz%')) ORDER BY w.timestampUNX") # AND (w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%')) 
rec = getTableSelect("SELECT w.timestmp,w.timestampUNX,w.city,w.temperature FROM Wetter w WHERE w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%') OR w.city LIKE ('%Belz%') ORDER BY w.timestampUNX") # AND (w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%')) 
print('Create dataframe')
data = pd.DataFrame.from_records(rec)
data.columns = ['Zeitstempel', 'Unix Zeitstempel', 'city', 'Temperatur']

print(data)

datamich = data.loc[data['city'] == 'Michendorf']
databln = data.loc[data['city'] == 'Berlin Schoeneberg']
databdblzg = data.loc[data['city'] == 'Bad Belzig']

figure(1)
plot(datamich['Unix Zeitstempel']/3600.,datamich['Temperatur'],color='blue', linewidth=1.0, snap=True)
plot(databln['Unix Zeitstempel']/3600.,databln['Temperatur'],color='green', linewidth=1.0, snap=True)
plot(databdblzg['Unix Zeitstempel']/3600.,databdblzg['Temperatur'],color='peru', linewidth=1.0, snap=True)
grid(True)

'''
figure(2)
plot(datamich['Unix Zeitstempel'],datamich['Zeitdifferenz in s'],color='blue', linewidth=1.0, snap=True)
plot(databln['Unix Zeitstempel'],databln['Zeitdifferenz in s'],color='green', linewidth=1.0, snap=True)
grid(True)
show()
'''

show()