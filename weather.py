
from jsonhelper import *
from datetime import datetime, timedelta
import pandas as pd

class weather:
	def __init__(self, jsonvalues, cty):
		self.cityid = cty['FKID']

		self.city = jsonvalues['name']
		self.timestamp = datetime.utcfromtimestamp(jsonvalues['dt'])
		self.timestampRAW = jsonvalues['dt']
		self.begin, self.end = self.timestamptotimerange()
		self.sunrise = jsonvalues['sys']['sunrise']
		self.sunset = jsonvalues['sys']['sunset']
		self.country = jsonvalues['sys']['country']		

		self.descrid = jsonvalues['weather'][0]['id']
		self.description = jsonvalues['weather'][0]['main']
		self.descriptiondetailed = jsonvalues['weather'][0]['description']

		try:
			self.temperature = "%.2f" % (jsonvalues['main']['temp'] - 273.15)
		except Exception as e:
			self.temperature = ''

		try:
			self.temperaturemin = "%.2f" % (jsonvalues['main']['temp_min'] - 273.15)
		except Exception as e:
			self.temperaturemin = None

		try:
			self.temperaturemax = "%.2f" % (jsonvalues['main']['temp_max'] - 273.15)
		except Exception as e:
			self.temperaturemax = None

		try:
			self.temperaturegefuehlt = "%.2f" % (jsonvalues['main']['feels_like'] - 273.15)
		except Exception as e:
			self.temperaturegefuehlt = ''

		try:
			self.humidity = str(jsonvalues['main']['humidity'])
		except Exception as e:
			self.humidity = ''

		try:
			self.clouds = str(jsonvalues['clouds']['all'])
		except Exception as e:
			self.clouds = ''
		
		try:
			self.rain = str(jsonvalues['rain']['1h'])
		except:
			self.rain = None

		try:
			self.snow1h = str(jsonvalues['snow']['1h'])
		except:
			self.snow1h = None

		try:
			self.snow3h = str(jsonvalues['snow']['3h'])
		except:
			self.snow3h = None

		try:
			self.pressure = str(jsonvalues['main']['pressure'])
		except Exception as e:
			self.pressure = ''

		try:
			self.windspeed = str(jsonvalues['wind']['speed'])
		except Exception as e:
			self.windspeed = None

		try:
			self.winddeg = str(jsonvalues['wind']['deg'])
		except Exception as e:
			self.winddeg = None

		try:
			self.windgust = str(jsonvalues['wind']['gust'])
		except Exception as e:
			self.windgust = None

		try:
			self.cloudiness = str(jsonvalues['clouds']['all'])
		except Exception as e:
			self.cloudiness = None

		try:
			self.timezone = jsonvalues['timezone']/3600
		except Exception as e:
			self.timezone = 0


	def toDataFrame(self):
		dta = [self.country,
		self.city, 
		self.timestampRAW,
		self.sunrise, 
		self.sunset, 
		self.descrid,
		self.temperature,
		self.temperaturemin,
		self.temperaturemax,
		self.temperaturegefuehlt,
		self.humidity,
		self.pressure,
		self.windspeed,
		self.winddeg,
		self.windgust,
		self.cloudiness,
		self.rain,
		self.snow1h,
		self.snow3h,
		self.timezone,
		self.cityid]
		df = pd.DataFrame(dta)
		cols = ['country', 'city', 'timestampUNX', 'sunrise', 'sunset', 'descrid', 
                                'temperature', 'temperaturemin', 'temperaturemax', 'temperaturegefuehlt', 'humidity', 'pressure', 
                                'windspeed', 'winddeg', 'windgust', 'cloudiness', 'rain1h', 'snow1h', 'snow3h', 'timezone', 'ctyid']
		df.columns = cols			
		return df
		
		
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
		k += '  Wetter: ' + self.description + ' - ' + self.descriptiondetailed + '\n'
		#k += 'UTC: ' + self.timestamp.strftime('%d.%m.%Y %H:%M:%S') + ', Intervall von: ' + self.begin.strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + self.end.strftime('%d.%m.%Y %H:%M:%S') + '\n'
		#k += 'LOC: ' + (self.timestamp+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S')
		#k += ', Intervall von: ' + (self.begin+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', bis: ' + (self.end+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + '\n'
		k += '  Temperatur: ' + str(self.temperature) + ' °C, Luftfeuchtigkeit: ' + str(self.humidity) + ' %, Luftdruck: ' + str(self.pressure) + ' hPa\n'
		k += '  Bewoelkung: ' + str(self.clouds) + ' %, Windgeschwindigkeit: ' + str(self.windspeed) + ' m/s , Windrichtung: ' + str(self.winddeg) + '°'
		k += '\n  LOC: ' + (self.timestamp+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', UTC: ' + (self.timestamp.strftime('%d.%m.%Y %H:%M:%S'))
		k += '\n  Sunrise: ' + (self.sunrise+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ', Sunset: ' + (self.sunset+timedelta(hours=self.timezone)).strftime('%d.%m.%Y %H:%M:%S') + ''
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

