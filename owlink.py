
import urllib.request
import requests
import json
import numpy as np
import math

from requests.models import Response
from weather import *
import time
import os
import sys
import visu

#from dbhelper import insertRow
import dbhelper as dbh



def getcty(cty):
	_headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
	_url = str(cty['request'])
	try:
		_response = requests.get(_url, headers=_headers, verify = False, timeout = dbh.settings('ConnectionTimeout'))   
		if not _response.ok:
			raise Exception('owlink.py - request failed with error code: {}, reason: '.format(Response.status_code, Response.reason))
		else:
			_parsed_json_Erhaltete_Werte  = json.loads(_response.text)
			wth  = weather(_parsed_json_Erhaltete_Werte,cty)
			return wth
	except Exception as e:
		raise e



def iterate_list():

	dct = {}

	dbh.Log("start visualisation...")
	hmi = visu.visualisation()
	hmi.start_visu()
	
	dbh.Log('start loop...')
	i = 0
	while True:
		ctylst = dbh.getCityTable()

		for index, cty in ctylst.iterrows():
			valid = False
			try:
				wth = getcty(cty)
				valid = True
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				dbh.Log('owlink.py - Error request: {} at line {}'.format(e, exc_tb.tb_lineno),'Error')

			if valid:
				if not cty['FKID'] in dct:
					dbh.Log("City {} added to observation query".format(cty["Name"]))
					try:
						dbh.insertRow(wth)
						dct[cty['FKID']] = { "tmstmp" : wth.timestampRAW, "response" : 'False'}
					except Exception as e:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						dbh.Log('owlink.py - Error during process: {} at line {}'.format(e, exc_tb.tb_lineno),'Error')
				else:
					try:
						tmstmp = wth.timestampRAW
						if dct[cty['FKID']]['tmstmp'] != tmstmp: 
							dbh.insertRow(wth)
							dct[cty['FKID']] = { "tmstmp" : wth.timestampRAW, "response" : 'False'}
					except Exception as e:
						exc_type, exc_obj, exc_tb = sys.exc_info()
						dbh.Log('owlink.py - Error during process: {} at line {}'.format(e, exc_tb.tb_lineno),'Error')

				hmi.updatevisu()
				
			time.sleep(dbh.settings('TimeToNextLocationRequest')/1000.0)

		time.sleep(dbh.settings('TimeToNextLocationIteration')/1000.0)

		i += 1

	hmi.stop_visu()




print('initiate...')
if sys.platform == "linux" or sys.platform == "linux2":
    print('OS: Linux')
elif sys.platform == "darwin":
    print('OS: OS X')
elif sys.platform == "win32":
    print('OS: Windows')

time.sleep(2.0)

dbh.Log("database update if necessary (v{})...".format(dbh.databaseversion()))
print("database update if necessary (v{})...".format(dbh.databaseversion()))
import schemaupdate as su
su.runUpdate()
dbh.Log("database Version new: v{}".format(dbh.databaseversion()))
print("database Version new: v{}".format(dbh.databaseversion()))

print("run programm...")
dbh.Log("run programm...")
time.sleep(5.0)
try:
	iterate_list()
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	dbh.Log('owlink.py - Unknown handled Exception during iteration: {} at line {}'.format(e, exc_tb.tb_lineno),'Error')

