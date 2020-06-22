import pandas as pd
import sqlite3
from dbhelper import getTableSelect
import datetime as dt
from matplotlib.pyplot import *

print('Read database...')

#rec = getTableSelect("SELECT w.timestmp,w.timestampUNX,w.city,w.temperature FROM Wetter w WHERE w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%') OR w.city LIKE ('%Belz%') ORDER BY w.timestampUNX") # AND (w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%')) 
#print('Create dataframe')
#data = pd.DataFrame.from_records(rec)

data = pd.read_sql_query("SELECT w.timestmp,w.timestampUNX,w.city,w.temperature FROM Wetter w WHERE w.city LIKE ('%Mich%') OR w.city LIKE ('%Schoe%') OR w.city LIKE ('%Belz%') ORDER BY w.timestampUNX",sqlite3.connect('wetter.db'))
data.columns = ['Zeitstempel', 'Unix Zeitstempel', 'city', 'Temperatur']
data['ts'] = data['Zeitstempel'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

print(data)

datamich = data.loc[data['city'] == 'Michendorf']
databln = data.loc[data['city'] == 'Berlin Schoeneberg']
databdblzg = data.loc[data['city'] == 'Bad Belzig']

figure(1)
plot(datamich['ts'],datamich['Temperatur'],color='blue', linewidth=1.0, snap=True)
plot(databln['ts'],databln['Temperatur'],color='green', linewidth=1.0, snap=True)
plot(databdblzg['ts'],databdblzg['Temperatur'],color='peru', linewidth=1.0, snap=True)
grid(True)

'''
figure(2)
plot(datamich['Unix Zeitstempel'],datamich['Zeitdifferenz in s'],color='blue', linewidth=1.0, snap=True)
plot(databln['Unix Zeitstempel'],databln['Zeitdifferenz in s'],color='green', linewidth=1.0, snap=True)
grid(True)
show()
'''

show()