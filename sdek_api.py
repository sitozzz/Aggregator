import requests
from xml.dom import minidom
from time import sleep
import xmltodict
import json

#  Request description
req = requests.get('https://integration.cdek.ru/pvzlist/v1/xml')
req = req.text
# XML to JSON
data = xmltodict.parse(req)
data = json.dumps(data)
data = json.loads(data)
print(data['PvzList']['Pvz'][0])

# JSON to XML
test_response = {
    'key1':
    {
        'key11':'value1',
        'key12':'value2'
    }
}
test_response = xmltodict.unparse(test_response, pretty=True)
print(test_response)