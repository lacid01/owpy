
from jsonhelper import *
from datetime import datetime, timedelta

class weather:
	def __init__(self, jsonvalues):
		self.city = jsonvalues['name']
		self.timestamp = datetime.utcfromtimestamp(jsonvalues['dt'])
		self.begin, self.end = self.timestamptotimerange()
		self.sunrise = datetime.utcfromtimestamp(jsonvalues['sys']['sunrise'])
		self.sunset = datetime.utcfromtimestamp(jsonvalues['sys']['sunset'])
		self.country = jsonvalues['sys']['country']		

		self.description = jsonvalues['weather'][0]['main']

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
		k += 'Wetter: ' + self.description + '\n'
		k += 'UTC: ' + self.timestamp.strftime('%d.%m.%Y %H:%M:%S') + ', Intervall von: ' + self.begin.strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + self.end.strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'LOC: ' + (self.timestamp+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S')
		k += ', Intervall von: ' + (self.begin+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + (self.end+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'Sunrise: ' + (self.sunrise+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', Sunset: ' + (self.sunset+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += 'Temperatur: ' + str(self.temperature) + ', Luftfeuchtigkeit: ' + str(self.humidity) + ', Luftdruck: ' + str(self.pressure) + '\n'
		k += 'Bewoelkung: ' + str(self.clouds) + ', Windgeschwindigkeit: ' + str(self.windspeed) + ', Windrichtung: ' + str(self.winddeg)
		return k


	def getjsondata(self, datapointid, value):
		rt = {
			"datapointid": datapointid,
			"Values": jsonhelper.valuetojson(value, self.begin, self.end)
		}
		return rt

	def getjsondatalist(self, target):
		"""
		target:
        "temperature": "dpid",
        "humidity": "dpid",
        "pressure": "dpid",
        "windspeed": "dpid",
        "winddegree": "dpid"
		"""
		rt = [
            self.getjsondata(target['temperature'],self.temperature),
            self.getjsondata(target['humidity'],self.humidity),
            self.getjsondata(target['pressure'],self.pressure),
            self.getjsondata(target['windspeed'],self.windspeed),
            self.getjsondata(target['winddegree'],self.winddeg)
		]
		return rt

