# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import sqlite3
from dbhelper import getTableSelect
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# %%
city = ['Michendorf', 'Oslo','Grundtjärn', 'Longyearbyen']
ct = """c.cityname = '""" + """' OR c.cityname = '""".join(city) + """'"""
print(ct)


# %%
query = """SELECT c.cityname as city, w.sur, w.sus, w.ts FROM Cities c
INNER JOIN 
(SELECT DISTINCT round((timestampUNX+timezone*3600)/3600/24)*3600*24 as ts, sunrise+timezone*3600 as sur, sunset+timezone*3600 as sus, ctyid FROM Wetter WHERE sunrise < sunset) w
ON w.ctyid = c.ctyid
WHERE {} ORDER BY w.ts""".format(ct)
print(query)
data = pd.read_sql_query(query,sqlite3.connect('wetter.db'))
print(data.columns)


# %%
data['sur_dt'] = data.apply(lambda x : (int(datetime.utcfromtimestamp(x['sur']).strftime('%H'))+int(datetime.utcfromtimestamp(x['sur']).strftime('%M'))/60), axis=1)
data['sus_dt'] = data.apply(lambda x : int(datetime.utcfromtimestamp(x['sus']).strftime('%H'))+int(datetime.utcfromtimestamp(x['sus']).strftime('%M'))/60, axis=1)
data['ts_dt'] = data.apply(lambda x : datetime.utcfromtimestamp(x['ts']), axis=1)
data['ts_year'] = data.apply(lambda x : (datetime.utcfromtimestamp(x['ts']).strftime('%Y')), axis=1)

#print(data)

dta = []
for cty in city:
    dta_temp = data[(data["city"] ==cty) & (data['ts_year'] == '2021')]
    dta_temp['sur_dt_diff'] = dta_temp['sur_dt'].rolling(window=4).apply(lambda x: (x[1] - x[0] + x[2] - x[1] + x[3] - x[2])/3)
    dta_temp['sus_dt_diff'] = dta_temp['sus_dt'].rolling(window=4).apply(lambda x: (x[1] - x[0] + x[2] - x[1] + x[3] - x[2])/3)
    dta.append(dta_temp)

# %%
#%%
#print(data[(data["city"] =="Longyearbyen") & (data['ts_year'] == '2021')])

clrs = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple']
clr_idx = 0
plt.figure(1)
plt.subplot(1,2,1)
for _dta in dta:
    cty = _dta.iloc[0]['city']
    plt.plot(_dta['ts_dt'],_dta['sur_dt'],
        clrs[clr_idx], label=cty)
    plt.plot(_dta['ts_dt'],_dta['sus_dt'],
        clrs[clr_idx], label='')
    clr_idx = clr_idx + 1
plt.legend()
plt.grid(True)
plt.ylim([0,24])
plt.yticks([i*2 for i in range(13)])

clr_idx = 0
plt.subplot(1,2,2)
for _dta in [dta[0]]:
    cty = _dta.iloc[0]['city']
    plt.plot(_dta['ts_dt'],_dta['sur_dt_diff'],
        clrs[clr_idx], label=cty)
    #plt.plot(_dta['ts_dt'],_dta['sus_dt_diff'],
    #    clrs[clr_idx], label='')
    clr_idx = clr_idx + 1
plt.legend()
plt.grid(True)
plt.show()
