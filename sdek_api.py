import requests
import json
# TODO: Change this
# test_login = "3y03Ahh2XigMgzN1l7mWff6jZMSCqHE1"
# test_pswd = dateExecute + "&Or6kB0BaKUrGCx51NWtVNcZ4YmVRFMBN"
prod_login = "9PNdW6RZ7Klnfg2P4JXkglM9BkznKrzh"
prod_pswd = "RfYDInLNGtB654BaZi8Z11ylwwq4WBmO"

def calculate_sdek(data, sdek_id):
	sdek_json = {
		"version":"1.0",
		"dateExecute": data['dateExecute'], 
		# "authLogin": prod_login, 
		# "secure": prod_pswd, 
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