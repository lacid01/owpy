
import urllib.request
import requests
import json
import numpy as np
import math
from weather import *
import time
import os


from targetrawdatapoint import *



def getcty(cty):
	lat = str(cty['lat'])
	lon = str(cty['lon'])

	_headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
	_url='http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=53dafd10eab9188765711009650ab647'
	_response = requests.get(_url, headers=_headers, verify = False)   
	_parsed_json_Erhaltete_Werte  = json.loads(_response.text)

	#print(_parsed_json_Erhaltete_Werte)

	wth  = weather(_parsed_json_Erhaltete_Werte)
	return wth

def postcty(wth, cty):
	vals = wth.getjsondatalist(cty)

	#print(wth)

	rt = []
	for val in vals:
		header ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
		posturl = "http://eneffco/EnEffCoPKr/api/v0.1/rawdatapoint/" + val['datapointid'] + "/values?comment=warum"
		rt.append(requests.post(posturl, data = val['Values'], headers=header, verify = False, auth=('EnEffCoSystemadmin', 'EnEffCoOekotec')))
		#print('ID: ' + val['datapointid'])
		#print("Values: " + val['Values'])

	return rt,wth.city,wth.begin


def iterate_list(ctylst):

	dct = {}

	
	for cty in ctylst:
		wth = getcty(cty)
		rsp,city,bgn = postcty(wth, cty)
		dct[cty['ID']] = { "begin" : bgn, "response" : rsp}
		print('\n\n' + str(wth))
		time.sleep(1.0)
	
	i = 0
	while True:

		print('i: ' + str(i) + ', dt: ' + str(datetime.now()))
		for cty in ctylst:
			wth = getcty(cty)
			bgn = wth.begin
			if dct[cty['ID']]['begin'] != bgn:
				rsp,city,bgn = postcty(wth, cty)
				dct[cty['ID']] = { "begin" : bgn, "response" : rsp}
				print('\n\n' + str(wth))
			time.sleep(1.0)

		time.sleep(5.0)

		i += 1



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

print('STARTE...')

ctlist = datapointtarget.get_cities()
iterate_list(ctlist)


#k,cty,begin = postcty(getcty( datapointtarget.get_sbrg() ), datapointtarget.get_sbrg() )
#print(k)
#print(cty + ', ' + str(begin))
#print(begin == begin)

