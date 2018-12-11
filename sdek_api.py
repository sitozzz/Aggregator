import requests
import json
import xmltodict
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
		{"id":1, "priority" : 10},
		{"id":139, "priority" : 1},
		{"id":293, "priority" : 1},
		{"id":18, "priority" : 9},
		{"id":3, "priority" : 1}
		]

	storage_to_storage = [
		{"id":136, "priority" : 1},
		{"id":234, "priority" : 1},
		{"id":291, "priority" : 1},
		{"id":5, "priority" : 1},
		
		{"id":62, "priority" : 1},
		{"id":63, "priority" : 1},

		{"id":10, "priority" : 1},
		{"id":15, "priority" : 1},

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

def get_pvz_list(city_id):
	# city_id = str(city_id)
	url = 'http://integration.cdek.ru/pvzlist/v1/xml?weightmax=50&cityid={0}&allowedcod=1'.format(city_id)
	sdek_res = requests.get(url)
	# print(sdek_res)
	sdek_res = xmltodict.parse(sdek_res.text)
	data = sdek_res['PvzList']
	output = []
	for pvz in data:
		for el in data[pvz]:
			pvz_json = {}

			print(el['@PostalCode'])
			pvz_json['display_name'] = el['@Name'] + '-' + el['@PostalCode']
			pvz_json['postal_code'] = el['@PostalCode']
			pvz_json['full_address'] = el['@FullAddress']
			pvz_json['code'] = el['@Code']
			output.append(pvz_json)
	
	print(output)
	return output

			
	# for el in data:
	# 	for e in data[el]:
	# 		print(e)
	# 	break

def add_delivery():
	url = 'https://integration.cdek.ru/addDeliveryRaw'
	headers = {'Content-Type': 'application/xml'} 
	
	xml = '<?xml version="1.0" encoding="UTF-8"?><deliveryrequest account="716b2c7e8f2e1a46ff8fd126adaef97d" currency="rub" date="2017-03-15 10:17:07" foreigndelivery="false" number="test_request" ordercount="2" secure="4180a7f32c5f605db27f15e26eec03d7"> <order clientside="SENDER" comment="test_comment" number="number2017_6344227223" phone="123456789123456789" reccitycode="44" recipientcompany="company-6344227223" recipientcurrency="rub" recipientemail="email_1_G4Akh0@test.ru" recipientname="Получатель Получателев" sendcitycode="44" tarifftypecode="1"> <address flat="flat-G4Akh0" house="house-G4Akh0" street="street-G4Akh0"/> <sender name="Отправ Отправителев"> <address flat="flat-G4Akh0" house="house-G4Akh0" street="street-G4Akh0"/> <phone>+7-913-873-98-76</phone> <phone>7-913-287-39-10</phone> </sender> <package barcode="test_package" comment="test_comment" sizea="10.0" sizeb="20.0" sizec="30.0" weight="1000.0"/> </order> <order clientside="SENDER" comment="test_comment" number="number2017_6344227225" phone="123456789 123456789" reccitycode="44" recipientcompany="company-6344227225" recipientcurrency="rub" recipientemail="email_1_G4Akh1@test.ru" recipientname="Получатель Получателев" sendcitycode="44" tarifftypecode="1"> <address flat="flat-G4Akh1" house="house-G4Akh1" street="street-G4Akh1"/> <sender name="Отправ Отправителев"> <address flat="flat-G4Akh1" house="house-G4Akh1" street="street-G4Akh1"/> <phone>89133309944</phone> <phone>89138092416</phone> </sender> <package barcode="test_package" comment="test_comment" sizea="10.0" sizeb="20.0" sizec="30.0" weight="1000.0"/> </order></deliveryrequest>'


	res = requests.post(url = url, data = xml.encode('utf-8'), headers = headers)
	print(res.text)

add_delivery()
