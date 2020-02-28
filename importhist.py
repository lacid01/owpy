import pandas as pd
import os, pytz
from datetime import datetime, timedelta

path = os.path.dirname(os.path.abspath(__file__))

try:
    #data = pd.read_csv('C:\\MyProjects\\foodpinch-pinch-analyse-f-r-dz\\db\\stoffstroeme.csv')
    data = pd.read_csv(path + '/auseec/sbrg.csv', delimiter=';')
    data['Messzeit'] = data['Messzeit'].apply(lambda x: datetime.strptime(x, '%d.%m.%y %H:%M').strftime('%Y-%m-%d %H:%M:%S')  )
    data['UNIX Zeitstempel'] = data['Messzeit'].apply(lambda x: str(int(datetime.strptime(x, '%Y-%m-%d %H:%M:%S').astimezone(pytz.utc).timestamp()) ))
    data['Windgeschwindigkeit (m/s)'] = data['Windgeschwindigkeit (m/s)'].apply(lambda x: x.replace(',','.'))
    data['Sonnenaufgang'] = data['Sonnenaufgang'].apply(lambda x: '2000-01-01 ' + x)
    data['Sonnenuntergang'] = data['Sonnenuntergang'].apply(lambda x: '2000-01-01 ' + x)
    data['Temperatur (°C)'] = data['Temperatur (°C)'].apply(lambda x: x.replace(',','.'))
    data['Luftfeuchtigkeit (%)'] = data['Luftfeuchtigkeit (%)'].apply(lambda x: str(x).replace(',','.'))
    data['Luftdruck (hpa)'] = data['Luftdruck (hpa)'].apply(lambda x: str(x).replace(',','.'))
    data['Windrichtung (Deg)'] = data['Windrichtung (Deg)'].apply(lambda x: str(x).replace(',','.'))
    print(data.drop(labels=['Unnamed: 0'], axis=1))
    print()
except Exception as e:
    print(e) 
    rd = input('Beende mit Enter')
