import requests
import json
# TODO: Change this
# test_login = "3y03Ahh2XigMgzN1l7mWff6jZMSCqHE1"
# test_pswd = dateExecute + "&Or6kB0BaKUrGCx51NWtVNcZ4YmVRFMBN"
prod_login = "9PNdW6RZ7Klnfg2P4JXkglM9BkznKrzh"
prod_pswd = "RfYDInLNGtB654BaZi8Z11ylwwq4WBmO"

'''
Sdek usable tariffs:

Посылка c-c 136, 
Посылка c-д 137,
Посылка д-c 138, 
Посылка д-д 139, 

Экономичная посылка с-д 233,  
Экономичная посылка с-с 234,  

До постомата ???,  

CDEK Express с-с 291 ,
CDEK Express д-д 293, 
CDEK Express с-д 294, 
CDEK Express д-с 295, 

Китайский экспресс,  

Экспресс лайт ,   
Супер-экспресс до 18, 
Экономичный экспресс, 
Супер-экспресс до 12,
Магистральный экспресс
'''
def select_delivery_type(type_from, type_to):
	# ===Tariffs ids===
	door_to_door = [
		{"id":139, "priority" : 1},
		{"id":293, "priority" : 1},
		{"id":18, "priority" : 1},
		{"id":1, "priority" : 1},
		{"id":3, "priority" : 1}
		]

	storage_to_storage = [
		{"id":136, "priority" : 1},
		{"id":234, "priority" : 1},
		{"id":291, "priority" : 1},
		{"id":5, "priority" : 1},
		{"id":15, "priority" : 1},
		{"id":62, "priority" : 1},
		# {"id":3, "priority" : 1}
		]

	door_to_storage = [
		{"id":138, "priority" : 1},
		{"id":295, "priority" : 1},
		{"id":17, "priority" : 1},
		{"id":12, "priority" : 1},
		# {"id":3, "priority" : 1}
		]

	storage_to_door = [
		{"id":137, "priority" : 1},
		{"id":233, "priority" : 1},
		{"id":294, "priority" : 1},
		{"id":11, "priority" : 1},
		{"id":16, "priority" : 1},
		# {"id":3, "priority" : 1}
		]
	# ===Tariffs ids===
	if type_from == 'door' and type_to == 'door':
		return door_to_door
	elif type_from == 'door' and type_to == 'storage':
		return door_to_storage
	elif type_from == 'storage' and type_to == 'door':
		return storage_to_door
	else:
		return storage_to_storage

def calculate_sdek(data):
	# print(data)
	# if data['goods']['volume'] == None:
	# 	data['goods'].pop("volume")
	# else:
	# 	data['goods'].pop("height")
	# 	data['goods'].pop("length")
	# 	data['goods'].pop("width")

	sdek_json = {
		"version":"1.0",
		"dateExecute": data['dateExecute'], 
		# "authLogin": prod_login, 
		# "secure": prod_pswd, 
		"senderCityId": data['city1']['id'], 
		"receiverCityId": data['city2']['id'], 
		# Check this
		# "tariffId": sdek_id,
		# TEST!!!! 
		"tariffList": select_delivery_type(data['deliveryType']['deliveryFrom'], data['deliveryType']['deliveryTo']), 
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
	sdek_res = json.loads(sdek_res.text,encoding='utf-8')
	print(sdek_res)
	return sdek_res