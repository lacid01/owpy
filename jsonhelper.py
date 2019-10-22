class jsonhelper:

	@staticmethod
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

	@staticmethod
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