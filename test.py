import urllib.request
import requests
import json  
import pandas as pd  
from pandas.io.json import json_normalize  

_headers ={ 'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization':'*/*'}
_url='http://api.openweathermap.org/data/2.5/weather?lat=52.482626&lon=13.357410&appid=53dafd10eab9188765711009650ab647'
_response = requests.get(_url, headers=_headers, verify = False)   
_parsed_json_Erhaltete_Werte  = json.loads(_response.text)


df = json_normalize(_parsed_json_Erhaltete_Werte['weather']) 

print(json_normalize(_parsed_json_Erhaltete_Werte['coord']) )
print(json_normalize(_parsed_json_Erhaltete_Werte['weather']) )
print(json_normalize(_parsed_json_Erhaltete_Werte['main']) )
print(json_normalize(_parsed_json_Erhaltete_Werte['wind']) )
print(json_normalize(_parsed_json_Erhaltete_Werte['clouds']) )
print(json_normalize(_parsed_json_Erhaltete_Werte['sys']) )
print(pd.read_json(_parsed_json_Erhaltete_Werte['timezone']) )