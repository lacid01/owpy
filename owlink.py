
import urllib.request
import requests
import json
import numpy as np
import math
from weather import *
import time
import os
import sys
import visu

#from dbhelper import insertRow
import dbhelper as dbh



def getcty(cty):
	lat = str(cty['lat'])
	lon = str(cty['lon'])

	_headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
	_url='http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=53dafd10eab9188765711009650ab647'
	_response = requests.get(_url, headers=_headers, verify = False)   
	_parsed_json_Erhaltete_Werte  = json.loads(_response.text)

	#print(_parsed_json_Erhaltete_Werte)

	wth  = weather(_parsed_json_Erhaltete_Werte,cty)
	return wth


def weatherToDb(wth):
	dbh.insertRow(wth)


def iterate_list():

	dct = {}

	hmi = visu.visualisation()
	hmi.start_visu()
	
	i = 0
	while True:
		
		ctylst = dbh.getCityTable()

		print('i: ' + str(i) + ', dt: ' + str(datetime.now()))
		for index, cty in ctylst.iterrows():
			if not cty['ID'] in dct:
				wth = getcty(cty)
				weatherToDb(wth)
				hmi.updatevisu()
				dct[cty['ID']] = { "tmstmp" : wth.timestampRAW, "response" : 'False'}
				time.sleep(1.0)
			else:
				try:
					wth = getcty(cty)
					tmstmp = wth.timestampRAW
					if dct[cty['ID']]['tmstmp'] != tmstmp: # Hier fehlt eine abfrage bei neu hinzugefuegter city
						#if cty['Zeige in Visu'] == 'True':
						#	hmi.add_weather_to_queu(wth)
						weatherToDb(wth)
						hmi.updatevisu()
						dct[cty['ID']] = { "tmstmp" : tmstmp, "response" : 'False'}
					time.sleep(1.0)
				except Exception as e:
					print("Keine Verbindung zu ow!")

		time.sleep(60.0)

		i += 1

	hmi.stop_visu()



#headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
#url='http://api.openweathermap.org/data/2.5/weather?lat=52.482626&lon=13.357410&appid=53dafd10eab9188765711009650ab647'
#response = requests.get(url, headers=headers, verify = False)   
#parsed_json_Erhaltete_Werte  = json.loads(response.text)
#print(parsed_json_Erhaltete_Werte)
#print('\n\n')

#k = weather(parsed_json_Erhaltete_Werte)
#print(k)


#print('\nSchreibe nach EnEffCo:')
#print(k.gettempjson())

"""
hmi = visu.visualisation()
time.sleep(1.0)
print('Starte runner der hmi')
hmi.start_visu()
time.sleep(1.0)
print('Fuege 5.0 hinzu')
idx = 0
while idx < 20:
	hmi.add_weather_to_queu(idx)
	time.sleep(0.2)
	idx += 2
time.sleep(5.0)
hmi.stop_visu()

sys.exit()
"""

print('STARTE...')
if sys.platform == "linux" or sys.platform == "linux2":
    print('OS: Linux')
elif sys.platform == "darwin":
    print('OS: OS X')
elif sys.platform == "win32":
    print('OS: Windows')

time.sleep(5.0)


iterate_list()


#k,cty,begin = postcty(getcty( datapointtarget.get_sbrg() ), datapointtarget.get_sbrg() )
#print(k)
#print(cty + ', ' + str(begin))
#print(begin == begin)

