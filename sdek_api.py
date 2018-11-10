import requests
from time import sleep
import xmltodict
import json
import hashlib
test_login = "3y03Ahh2XigMgzN1l7mWff6jZMSCqHE1"
dateExecute = "2018-12-12"
test_pswd = dateExecute + "&Or6kB0BaKUrGCx51NWtVNcZ4YmVRFMBN"

req = { 
	"version":"1.0",
	"dateExecute":"2012-07-27", 
	"authLogin":test_login, 
	"secure": hashlib.md5(test_pswd.encode('utf-8')).hexdigest(), 
	"senderCityId":"270", 
	"receiverCityId":"44", 
	"tariffId":"137", 
	"goods": 
		[ 
			{ 
				"weight":"0.3", 
				"length":"10", 
				"width":"7", 
				"height":"5" 
			}, 
			{ 
				"weight":"0.1", 
				"volume":"0.1" 
			} 
		],
	"services": [
		{	
			"id": 2,	
			"param": 2000	
		},
		{	
			"id": 30
		}
	]
} 	

# result = requests.get


# #  Request description
# req = requests.get('https://integration.cdek.ru/pvzlist/v1/xml')
# req = req.text
# # XML to JSON
# data = xmltodict.parse(req)
# data = json.dumps(data)
# data = json.loads(data)
# print(data['PvzList']['Pvz'][0])

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
sdek_json = {
        "version":"1.0",
        "dateExecute":"2012-07-27", 
        # "authLogin":"098f6bcd4621d373cade4e832627b4f6", 
        # "secure":"396fe8e7dfd37c7c9f361bba60db0874", 
        "senderCityId":"270", 
        "receiverCityId":"1071", 
        "tariffId":"11", 
        "goods": [ 
            { 
                "weight":"0.3", 
                "length":"10", 
                "width":"7", 
                "height":"5" 
            }
           
        ],
        # "services": [
        #     {	
        #         "id": 2,	
        #         "param": 2000	
        #     },
        #     {	
        #         "id": 30
        #     }
        # ]
    }

sdek_res = requests.post('http://api.cdek.ru/calculator/calculate_price_by_json.php',json=sdek_json)
txt = sdek_res.text
txt = json.loads(txt)
print(txt)