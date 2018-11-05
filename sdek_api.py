import requests
from xml.dom import minidom
from time import sleep
import xmltodict
import json


#  Request description
req = requests.get('https://integration.cdek.ru/pvzlist/v1/xml')
req = req.text
data = xmltodict.parse(req)
data = json.dumps(data)
data = json.loads(data)
print(data['PvzList']['Pvz'][0])
