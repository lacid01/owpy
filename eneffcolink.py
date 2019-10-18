
import urllib.request
import requests
import json
import numpy as np
import math

class eneffco:


	def __init__(self, server, user, pw):
		self.server = server + '/api/v0.1'
		self.user = user
		self.pw = pw
		self.headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}

		# Lade Datenpunktliste
		url_zu_datenpunktliste = self.server + '/datapoint'
		self.datenpunktliste  = json.loads(self.request_ausfuehren(url_zu_datenpunktliste).text)



	def request_ausfuehren(self, url):
		return requests.get(url, headers=self.headers, verify = False, auth=(self.user, self.pw))


	def get_datapoint_list_as_dict(self):		
		return self.datenpunktliste


	def datapoint(self, datapoint):
		dp = ''
		idx = 0
		while len(dp) == 0 & idx < len(self.datenpunktliste):
			if self.datenpunktliste[idx]['Code'] == datapoint:
				dp = self.datenpunktliste[idx]
			idx = idx + 1
		return dp


	def datapoint2(self,datapoints):
		ret = []
		for datapoint in datapoints:
			ret.append( self.datapoint(datapoint) )
		return ret


	def get_timeseries(self, datapoint, tfrom, tto, aggr):
		url_zu_wert = self.server + '/datapoint/' + datapoint['Id'] + '/timeseries?from=' + tfrom + 'T00%3A00%3A00.000Z&to=' + tto + 'T00%3A00%3A00.000Z&timeInterval=' + aggr
		werteliste  = json.loads(self.request_ausfuehren(url_zu_wert) .text)

		# TEST
		#k = timeseries(werteliste)
		#print(k[2])

		return timeseries(werteliste, datapoint)


	def timeseries2(self, datapoints, tfrom, tto, aggr):
		ret = []
		for datapoint in datapoints:
			ret.append( self.get_timeseries(datapoint, tfrom, tto, aggr) )
		return ret


	def timeseries_valarray(self, datapoint, tfrom, tto, aggr):
		timeseries = self.get_timeseries(datapoint,tfrom,tto,aggr)
		return timeseries.get_values_without_nan()

	"""
	returns nxm nd array
	"""
	def timeseries_valarray2(self, datapoints, tfrom, tto, aggr):
		"""
		returns nxm nd array
		"""
		_timeseries = self.timeseries2(datapoints, tfrom, tto, aggr)
		y = []
		for timeseries in _timeseries:
			y.append( timeseries.get_values() )

		cols,rows = np.shape(y)
		y = np.transpose(y)

		ret = []
		for row in y:
			t = True
			for val in row:
				if val == 'NaN':
					t = False
			if t:
				ret.append(row.astype(float))
		return np.asarray(ret)






class timeseries:

	def __init__(self, series, description):
		_series = []
		for s in series:
			_series.append( timecontainer(s) )
		self.series = _series
		self.description = description

	def get_values(self):
		x = []
		for cont in self.series:
			x.append( cont.get_value())
		return np.asarray(x)

	def get_values_without_nan(self):
		x = []
		for cont in self.series:
			if not cont.isnan():
				x.append( cont.get_value() )
		return np.asarray(x)

	def clear_from_nan(self):
		x = []
		for value in self.series:
			if not value.isnan():
				x.append( value )
		self.series = x

	def align(self, other):
		x = []
		for i in range(self.series):
			if self.series[i].isnan() | other.series[i].isnan():
				x.append(i)
		#
		#
		#
		# NOCH NICHT FERTIG IMPLEMENTIERT
		#
		#

	def __str__(self):
		ret = '[\n'
		for con in self.series:
			ret = ret + str(con) + '\n'
		ret = ret + ']'
		return ret

	def __getitem__(self, k):
		return self.series[k]

	#def __add__(self, other):







class timecontainer:

	def __init__(self, container):
		if container['Value'] != 'NaN':
			if isinstance(container['Value'], float):
				self.value = container['Value']
			else:
				self.value = container['Value'].astype(float)
		else:
			self.value = math.nan
		self.tFrom = container['From']
		self.tTo = container['To']


	def __eq__(self, other):
		if self.isnan() & other.isnan():
			return True
		elif  self.isnan() | other.isnan():
			return False
		elif self.value == other.value:
			return True
		else:
			return False

	def __ne__(self, other):
		return not self == other

	def __lt__(self, other):
		return self.value < other.value

	def __le__(self, other):
		return self.value <= other.value

	def __gt__(self, other):
		return self.value > other.value

	def __ge__(self, other):
		return self.value >= other.value

	def __add__(self, other):
		if self.havesametime(other):
			return timecontainer(self.value + other.value, self.tFrom, self.tTo)
		else:
			return timecontainer(math.nan, self.tFrom, self.tTo)

	def __str__(self):
		return '[Value: ' + str(self.value) + ', From: ' + self.tFrom + ', To: ' + self.tTo + ']'

	def isnan(self):
		return math.isnan(self.value)

	def get_value(self):
		return self.value

	def havesametime(self,other):
		if self.tFrom == other.tFrom & self.tTo == other.tTo:
			return True
		else:
			return False