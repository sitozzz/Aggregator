import requests
from xml.dom import minidom
from time import sleep
import xmltodict
import json
import requests
from suds.client import Client
import simplejson
import codecs
import ast

client_number = 1020004365
client_key = '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'

f = open('dpd_cities.txt', 'r',encoding="utf8").read()
f = ast.literal_eval(f)

def get_cities():
    '''
    returns dict 
    orig_resp - object list (???)
    list - cities list that contains city properties

    '''

    url = "http://ws.dpd.ru/services/geography2?wsdl"
    client = Client(url)
    req_data = {}
    auth = {'clientNumber': 1020004365,
            'clientKey': '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'}
    req_data['auth'] = auth

    result = client.service.getCitiesCashPay(request=req_data)

    cities_arr = []
    for i in result:
        city = {}
        for key in i:
            city[key[0]] = key[1]
        cities_arr.append(city)
    f = open('dpd_cities.txt', 'w',encoding="utf8")
    
    #f = codecs.open('dpd_cities.txt', 'w', 'utf-16')
    simplejson.dump(cities_arr, f,ensure_ascii=False)
    f.close()
    return {'orig_resp': result, 'list': cities_arr}
def getCityProp(cityName):
    #global f
    print("-------------------")
    print(cityName)
    print(f[0])
    cityProp = {'cityName':cityName}
    for city in f:
        if city['cityName'] == cityName:
            cityProp = {'cityName':cityName, "cityId": city['cityId']}
    print(cityProp)
    print("-------------------")
    return cityProp
             
    

def get_service_cost(req):
    print('SDFSDFSDFSDFSDF')
    '''
    returns dict 
    orig_resp - object list (???)
    list - cities list that contains city properties

    '''
    
    
    from_city = req['city1']['name'].split(',')[0]
    to_city = req['city2']['name'].split(',')[0]
    if req['deliveryType']['deliveryFrom'] == 'storage':
        self_pickup = True
    else:
        self_pickup = False
    
    if req['deliveryType']['deliveryTo'] == 'storage':
        self_delivery = True
    else:
        self_delivery = False
    weight = req['goods'][0]['weight']

    if 'length' in req['goods'][0].keys():
        length = req['goods'][0]['length']
        width = req['goods'][0]['width']
        height = req['goods'][0]['height']
    else:
        length = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
        width = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
        height = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
    
 
    

    url = "http://ws.dpd.ru/services/calculator2?wsdl"
    client = Client(url)
    req_data = {}
    auth = {'clientNumber': 1020004365,
            'clientKey': '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'}
    pickup = getCityProp(from_city)
    
    delivery = getCityProp(to_city)

    req_data['auth'] = auth
    req_data['pickup'] = pickup
    req_data['delivery'] = delivery
    req_data['selfPickup'] = self_pickup
    req_data['selfDelivery'] = self_delivery
    req_data['serviceCode'] = 'ECN,CUR,NDY,PCL,DPI,DPE,MXO,ECU'
    req_data['parcel'] = {'weight':weight,'length':length,'width':width,'height':height}

    try:
        result = client.service.getServiceCostByParcels2(request=req_data)
    except Exception as identifier:
        print('DPD ERROR')
        return {'orig_resp': str(identifier) , 'list': str(identifier)}
        
    vrs = []
    for i in result:
        vr = {}
        for key in i:
            vr[key[0]] = key[1]
        vrs.append(vr)

    return {'orig_resp': result, 'list': vrs}

#get_cities()
#get_service_cost('кемерово','екатеринбург',True,True,1,20,20,20)



