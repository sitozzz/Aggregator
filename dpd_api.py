import requests
from xml.dom import minidom
from time import sleep
import xmltodict
import json

client_key = '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'

#  Request description
req = requests.get('http://wstest.dpd.ru/services/geography2?wsdl')
req = req.text
# XML to JSON
data = xmltodict.parse(req)
data = json.dumps(data)
data = json.loads(data)
#print(data)

import requests
url="http://wstest.dpd.ru/services/geography2?wsdl"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
body = """<ns:getCitiesCashPay><request><auth><clientNumber>1020004365</clientNumber><clientKey>04CD36DEDACCD77DB1424218BF57A57F6D82A12F</clientKey></auth><countryCode>?</countryCode></request></ns:getCitiesCashPay></soapenv:Envelope>"""




response = requests.post(url,data=body,headers=headers)
print (response.text)


# # JSON to XML
# test_response = {
#     'key1':
#     {
#         'key11':'value1',
#         'key12':'value2'
#     }
# }
# test_response = xmltodict.unparse(test_response, pretty=True)
# print(test_response)