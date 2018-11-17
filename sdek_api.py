import requests
import json
# TODO: Change this
test_login = "3y03Ahh2XigMgzN1l7mWff6jZMSCqHE1"
dateExecute = "2018-12-12"
test_pswd = dateExecute + "&Or6kB0BaKUrGCx51NWtVNcZ4YmVRFMBN"


def calculate_sdek(data, sdek_id):
	sdek_json = {
		"version":"1.0",
		"dateExecute": data['dateExecute'], 
		# "authLogin":"098f6bcd4621d373cade4e832627b4f6", 
		# "secure":"396fe8e7dfd37c7c9f361bba60db0874", 
		"senderCityId": data['city1']['id'], 
		"receiverCityId": data['city2']['id'], 
		# Check this
		"tariffId": sdek_id, 
		"goods": data['goods'],
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
	return sdek_res.text