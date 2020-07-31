from matplotlib.pyplot import axis
import pandas as pd
from requests_html import HTMLSession,HTML
from pprint import pprint
import sys, json, requests, sqlite3
import datetime as dt
from dateutil.relativedelta import relativedelta
from html.parser import HTMLParser
import html as hhtml
import historisch.eneffco as eec
import json
import matplotlib.pyplot as plt



dfs = pd.read_html("./historisch/brandenburg.html", thousands='.', decimal=",")

months = ['Januar','Februar','Maerz','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']

_df = dfs[0]
_df = _df.set_index('JahrYear').rename(columns={"WertValue":"Januar"})

data = _df

idx = 0
for df in dfs:
    if idx == 0:
        idx = 1
    else:
        _df = df
        _df = _df.set_index('JahrYear').rename(columns={"WertValue": months[idx]})
        #print(_df)
        data = pd.merge(data, _df, left_index=True, right_index=True, how='outer')
        idx = idx + 1

#print(data.T)


data['Jahresschnitt'] = data.apply(lambda row: sum(row)/12., axis=1)

print(data)

dta2 = data.copy()
dta2['gleitender Jahresschnitt'] = dta2['Jahresschnitt'].rolling(10, min_periods=2).mean()
dta2['Jahresminimum'] = dta2.apply(lambda row: min(row), axis=1)
dta2['gleitendes Jahresminimum'] = dta2['Jahresminimum'].rolling(10, min_periods=2).mean()
dta2['Jahresmaximum'] = dta2.apply(lambda row: max(row), axis=1)
dta2['gleitendes Jahresmaximum'] = dta2['Jahresmaximum'].rolling(10, min_periods=2).mean()
dta2 = dta2.drop(months,axis=1)

print(dta2)

plt.figure(1)
plt.plot(data.index, data['Jahresschnitt'])
plt.plot(dta2.index, dta2['gleitender Jahresschnitt'])
plt.plot(dta2.index, dta2['Jahresminimum'], color='lightblue')
plt.plot(dta2.index, dta2['gleitendes Jahresminimum'], color='blue')
plt.plot(dta2.index, dta2['Jahresmaximum'], color='pink')
plt.plot(dta2.index, dta2['gleitendes Jahresmaximum'], color='red')
plt.grid(True)

plt.figure(2)
dta = data.drop(2020).drop('Jahresschnitt',axis=1).T.apply(lambda row: sum(row)/140., axis=1).T
#print(dta)
plt.plot(dta)

#print(data.iloc[0])

plt.plot(data.loc[2019].drop('Jahresschnitt'))
plt.grid(True)
plt.show()


sys.exit()

eneffco = eec.Rawdatapointobject(server="http://eneffco/EnEffCoÖKOTEC",user="EnEffCoSystemadmin",pw="EnEffCoOekotec")
#print(eneffco.rohdatenpunktliste)

desc = eneffco.description('Berlin Brandenburg Temperatur historische Monatswerte dwd')
print(desc)

data_to_eneffco = data.drop('Jahresschnitt',axis=1).drop([1881+x for x in range(19)],axis=0)
new_col_names = {'Januar':'01.01.','Februar':'01.02.','Maerz':'01.03.','April':'01.04.','Mai':'01.05.','Juni':'01.06.',
'Juli':'01.07.','August':'01.08.','September':'01.09.','Oktober':'01.10.','November':'01.11.','Dezember':'01.12.'}
data_to_eneffco = data_to_eneffco.rename(columns=new_col_names)
print(data_to_eneffco)

time_from = []
time_to = []
value_data = []

for index,row in data_to_eneffco.iterrows():
    idx = []
    for _idx in row.index:
        idx.append(str(_idx) + '' + str(index))
        time_from.append(dt.datetime.strptime(str(_idx) + '' + str(index),'%d.%m.%Y').strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    idx2 = []
    for _idx in idx:
        idx2.append((dt.datetime.strptime(_idx,'%d.%m.%Y') - dt.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        time_to.append((dt.datetime.strptime(_idx,'%d.%m.%Y') + relativedelta(months=1) ).strftime('%Y-%m-%dT%H:%M:%S.000Z'))

    for entry in row:
        value_data.append(entry)

#print(value_data)
#print(time_to)

df_to_eneffco = pd.DataFrame(time_from,columns=['From'])
df_to_eneffco = df_to_eneffco.merge(pd.DataFrame(time_to,columns=['To']), left_index=True, right_index=True, how='outer')
df_to_eneffco = df_to_eneffco.merge(pd.DataFrame(value_data,columns=['Value']), left_index=True, right_index=True, how='outer')
#df_to_eneffco = df_to_eneffco.append(value_data)
#columns=['From','To','Value']
print(df_to_eneffco)

#print(eneffco.push_timeseries_to_eneffco('Berlin Brandenburg Temperatur historische Monatswerte dwd',df_to_eneffco[['Value','From','To']]).json)


