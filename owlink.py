
import urllib.request
import requests
import json
import numpy as np
import math
from datetime import datetime, timedelta

class jsonhelper:

	def convertdatetime(dt):
		y = str(dt.year)
		mo = dt.month
		d = dt.day
		h = dt.hour
		m = dt.minute

		if mo == 0:
			mo = '00'
		elif mo < 10:
			mo = '0' + str(mo)
		else:
			mo = str(mo)

		if d == 0:
			d = '00'
		elif d < 10:
			d = '0' + str(d)
		else:
			d = str(d)

		if h == 0:
			h = '00'
		elif h < 10:
			h = '0' + str(h)
		else:
			h = str(h)

		if m == 0:
			m = '00'
		elif m < 10:
			m = '0' + str(m)
		else:
			m = str(m)

		return y + '-' + mo + '-' + d + 'T' + h + ':' + m + ':00.000Z'


	def valuetojson(data,tfrom,tto):
		'''
		{
		  "Values": [
		    {
		      "Value": 0,
		      "From": "2019-10-18T10:05:53.030Z",
		      "To": "2019-10-18T10:05:53.030Z"
		    }
		  ]
		}
		'''
		ret = '{ \"Values\": [{'
		ret += '\"Value\" : ' + str(data) + ', '
		ret += '\"From\" : \"' +  jsonhelper.convertdatetime(tfrom) + '\", '
		ret += '\"To\" : \"' +  jsonhelper.convertdatetime(tto) + '\"'
		ret += '}]}'
		return ret


class weather:
	def __init__(self, jsonvalues):
		self.city = jsonvalues['name']
		self.timestamp = datetime.utcfromtimestamp(jsonvalues['dt'])
		self.begin, self.end = self.timestamptotimerange()
		self.sunrise = datetime.utcfromtimestamp(jsonvalues['sys']['sunrise'])
		self.sunset = datetime.utcfromtimestamp(jsonvalues['sys']['sunset'])
		self.country = jsonvalues['sys']['country']		

		try:
			self.temperature = "%.2f" % (jsonvalues['main']['temp'] - 273.15)
		except Exception as e:
			self.temperature = ''

		try:
			self.humidity = str(jsonvalues['main']['humidity'])
		except Exception as e:
			self.humidity = ''

		try:
			self.clouds = str(jsonvalues['clouds']['all'])
		except Exception as e:
			self.clouds = ''
		
		self.rain = 0

		try:
			self.pressure = str(jsonvalues['main']['pressure'])
		except Exception as e:
			self.pressure = ''

		try:
			self.windspeed = str(jsonvalues['wind']['speed'])
		except Exception as e:
			self.windspeed = ''

		try:
			self.winddeg = str(jsonvalues['wind']['deg'])
		except Exception as e:
			self.winddeg = ''

		try:
			self.timezone = jsonvalues['timezone']/3600
		except Exception as e:
			self.timezone = 0



		
		
	def timestamptotimerange(self):
		dt = self.timestamp
		dt_h = dt.hour
		dt_m = dt.minute

		if dt_m < 30:
			dt_ende = dt
			dt_m_anfang = 00
			dt_m_ende = 30
		else:
			dt_ende = dt  + timedelta(hours=1)
			dt_m_anfang = 30
			dt_m_ende = 00

		# datetime(year, month, day, hour, minute, second, microsecond)
		begin = datetime(dt.year, dt.month, dt.day, dt.hour, dt_m_anfang, 0, 0)
		end = datetime(dt_ende.year, dt_ende.month, dt_ende.day, dt_ende.hour, dt_m_ende, 0, 0)

		return begin,end
		

	def __str__(self):
		k = ''
		k += self.city + ', '
		k += self.country + '\n'
		k += 'UTC: ' + self.timestamp.strftime('%d.%m.%Y %H:%M:%S') + ', Intervall von: ' + self.begin.strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + self.end.strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'LOC: ' + (self.timestamp+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S')
		k += ', Intervall von: ' + (self.begin+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + (self.end+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'Sunrise: ' + self.sunrise.strftime('%d.%m.%Y %H:%M:%S') + ', Sunset: ' + self.sunset.strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'Temperatur: ' + str(self.temperature) + ', Luftfeuchtigkeit: ' + str(self.humidity) + ', Luftdruck: ' + str(self.pressure) + '\n'
		k += 'Bewoelkung: ' + str(self.clouds) + ', Windgeschwindigkeit: ' + str(self.windspeed) + ', Windrichtung: ' + str(self.winddeg)
		return k

	#def valuetojson(self):

	def gettempjson(self):
		return jsonhelper.valuetojson(self.temperature,self.begin,self.end)








headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
url='http://api.openweathermap.org/data/2.5/weather?lat=52.482626&lon=13.357410&appid=53dafd10eab9188765711009650ab647'
response = requests.get(url, headers=headers, verify = False)   
parsed_json_Erhaltete_Werte  = json.loads(response.text)
#print(parsed_json_Erhaltete_Werte)

k = weather(parsed_json_Erhaltete_Werte)
print(k)


print('\nSchreibe nach EnEffCo:')
print(k.gettempjson())

ladewerteurl = "http://eneffco/EnEffCoPKr/api/v0.1/rawdatapoint/145d7828-f6db-4dab-a4a1-1f929cb4892a/values?comment=peterpan2"
werte = requests.post(ladewerteurl, data = k.gettempjson(), headers=headers, verify = False, auth=('EnEffCoSystemadmin', 'EnEffCoOekotec')) #requests.get(ladewerteurl, headers=headers, verify = False, auth=('EnEffCoSystemadmin', 'EnEffCoOekotec'))   
print(werte)
#print(json.loads(werte.text))

