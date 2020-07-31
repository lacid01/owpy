
import urllib.request
import requests
import json
import math
from datetime import datetime, timedelta
import pandas as pd




"EnEffCo in Datapointobject umbenennen und in Rawdatapointobject. So können die Funktionen getrennt gehalten werden"

class Datapointobject:
	"""
	Konstruktor:
	- server : string  
	- user : string  
	- pw : string
	Attribute:
	- datenpunktliste : DataFrame  
	  
	Funktionen:
	- description
	- description2
	- timeseries
	- timeseries2
	- livevalue
	- livevalue2
	"""


	def __init__(self, server, user, pw):
		"""
		Erzeugt das Object EnEffCo.  
		Attribute:  
		- server : string  
		- user : string  
		- pw : string
		- datenpunktliste : DataFrame  
		"""
		self.server = server + '/api/v0.1'
		self.user = user
		self.pw = pw
		self.headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}

		self.datenpunktliste = pd.read_json(self.request_ausfuehren(self.server + '/datapoint') .text).set_index('Code')

	def request_ausfuehren(self, url):
		"""
		Fragt EnEffCo zu einer gegebenen url ab.  
		Gibt einen JSON String zurück.
		"""
		return requests.get(url, headers=self.headers, verify = False, auth=(self.user, self.pw))

	def request_post_ausfuehren(self, url, data):
		return requests.post(url, data = data, headers = self.headers, verify=False, auth=(self.user,self.pw))

	def convert_datetime_input(self,dt):
		if len(dt) >18:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		elif len(dt) > 15:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H:%M')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		elif len(dt) > 10:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		else:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')

	def check_if_datapointcode_exists(self,datapointcode):
		"""
		Prüft, ob ein Datenpunktcode in einer Datenpunktliste existiert. Gibt einen Bool zurück. (True/False)
		"""
		try:
			return self.datenpunktliste.loc[[datapointcode]].size > 0
		except:
			return False

	def description(self, datapoint):
		"""
		Gibt die Datenpunkteigenschaften zu einem gegebenen Datenpunktcode zurück als Pandas DataFrame
		"""
		dp = self.datenpunktliste.loc[[datapoint]]
		return dp

	def description2(self,datapoint):
		"""
		Gibt die Datenpunkteigenschaften zu mehreren gegebenen Datenpunktcodes zurück als Pandas DataFrame
		"""
		dp = self.description(datapoint[0])
		first = True
		for _dp in datapoint:
			if first:
				first = False
			else:
				dp = dp.append(self.description(_dp))
		return dp




	def timeseries(self, datapointcode, tfrom, tto, aggr, includeNaN = False):
		"""
		Eingabe: get_timeseries(datapointcode : string, tfrom : string, tto : string, aggr : string)   
		Gibt eine Zeitreihe als DataFrame zurück
		"""
		datapoint = self.description(datapointcode)

		url_zu_wert = self.server + '/datapoint/' + datapoint['Id'][datapointcode] + '/value?from=' + self.convert_datetime_input(tfrom) + '&to=' + self.convert_datetime_input(tto) + '&timeInterval=' + aggr + '&includeNanValues=false'
		df = pd.read_json(self.request_ausfuehren(url_zu_wert) .text)

		def calctimestamp(ts):
			return int((datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')-datetime(1970,1,1)).total_seconds())

		df['Timestamp'] = df['From'].apply(lambda x: calctimestamp(x)) 
		df = df.set_index('Timestamp')
		df = df[['From','To','Value']]
		return df

	def timeseries2(self, datapoints, tfrom, tto, aggr, includeNaN = False):
		"""
		Eingabe: get_timeseries(datapointcode : string[], tfrom : string, tto : string, aggr : string)   
		Gibt mehrere Zeitreihen als DataFrame zurück
		"""
		ret = self.timeseries(datapoints[0],tfrom,tto,aggr).rename(columns={"Value": datapoints[0]})
		first = False
		for datapoint in datapoints:
			if first:
				ret = pd.merge(ret, self.timeseries(datapoint, tfrom, tto, aggr).drop(columns = ['From','To']), left_index=True, right_index=True, how='inner').rename(columns={"Value": datapoint})
			else:
				first = True
		return ret

	def livevalue(self,datapointcode):
		'''
		Gibt den Livewert zu einem Datenpunktcode zurück als Pandas DataFrame
		'''
		datapoint = self.description(datapointcode)

		url_zu_wert = self.server + '/datapoint/' + datapoint['Id'][datapointcode] + '/live'
		df = pd.read_json('[' + self.request_ausfuehren(url_zu_wert) .text + ']')

		def calctimestamp(ts):
			return int((datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')-datetime(1970,1,1)).total_seconds())

		df['Timestamp'] = df['From'].apply(lambda x: calctimestamp(x)) 
		df = df.set_index('Timestamp')
		df['Datapointcode'] = datapointcode
		df = df[['From','To','LastUpdate','Datapointcode','Value']]
		df['Unit'] = datapoint['Unit'][datapointcode]
		df['BaseTime'] = datapoint['BaseTime'][datapointcode]

		return df

	def livevalue2(self,datapointcode):
		'''
		Gibt die Livewerte zu einer iterierbaren Datenpunktcodeliste zurück als Pandas DataFrame
		'''
		df = self.livevalue(datapointcode[0])
		if len(datapointcode) > 1:
			first = True
			for code in datapointcode:
				if first:
					first = False
				else:
					df = df.append(self.livevalue(code))

		return df


class Rawdatapointobject:

	def __init__(self, server, user, pw):
		"""
		Erzeugt das Object EnEffCo.  
		Attribute:  
		- server : string  
		- user : string  
		- pw : string
		- rohdatenpunktliste : DataFrame
		"""
		self.server = server + '/api/v0.1'
		self.user = user
		self.pw = pw
		self.headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}

		self.rohdatenpunktliste = pd.read_json(self.request_ausfuehren(self.server + '/rawdatapoint') .text).set_index('Name')

	def request_ausfuehren(self, url):
		"""
		Fragt EnEffCo zu einer gegebenen url ab.  
		Gibt einen JSON String zurück.
		"""
		return requests.get(url, headers=self.headers, verify = False, auth=(self.user, self.pw))

	def request_post_ausfuehren(self, url, data):
		return requests.post(url, data = data, headers = self.headers, verify=False, auth=(self.user,self.pw))

	def convert_datetime_input(self,dt):
		if len(dt) >18:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		elif len(dt) > 15:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H:%M')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		elif len(dt) > 10:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d %H')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')
		else:
			dt1_strp = datetime.strptime(dt, '%Y-%m-%d')
			return datetime.strftime(dt1_strp,'%Y-%m-%dT%H%%3A%M%%3A%S.000Z')

	def description(self, title):
		rdp = self.rohdatenpunktliste.loc[[title]]
		return rdp

	def description2(self, title):
		rdp = self.description(title[0])
		first = True
		for _rdp in title:
			if first:
				first = False
			else:
				rdp = rdp.append(self.description(_rdp))
		return rdp

	def timeseries(self, title, tfrom, tto, includeNaN = False):
		rawdatapoint = self.description(title)

		url_zu_wert = self.server + '/rawdatapoint/' + rawdatapoint['Id'][title] + '/value?from=' + self.convert_datetime_input(tfrom) + '&to=' + self.convert_datetime_input(tto) + '&includeNanValues=false'
		df = pd.read_json(self.request_ausfuehren(url_zu_wert) .text)

		def calctimestamp(ts):
			return int((datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')-datetime(1970,1,1)).total_seconds())

		df['Timestamp'] = df['From'].apply(lambda x: calctimestamp(x)) 
		df = df.set_index('Timestamp')
		df = df[['From','To','Value']]
		return df

	def timeseries2(self, title, tfrom, tto, includeNAaN = False):
		pass

	def livevalue(self, title):
		pass

	def livevalue2(self, title):
		pass

	def push_timeseries_to_eneffco(self, rawdatapointname, timeseries, comment = 'none'):
		'''
		Schreibt eine Zeitreihe in EnEffCo.  
		timeseries als Pandas DataFrame mit den Spalten: 'From', 'To', 'Value'
		'''
		first = True
		data = '{ "Values": ['
		for index, row in timeseries.iterrows():
			if first:
				data = data + row.to_json()
				first = False
			else:
				data = data + ',' + row.to_json()
		data = data + ']}'

		#print(data)

		rawdatapointid = self.rohdatenpunktliste.loc[rawdatapointname]['Id']
		return self.request_post_ausfuehren(self.server + '/rawdatapoint/' + rawdatapointid + '/value?comment=' + comment, data)



