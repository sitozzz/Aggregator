import requests
from xml.dom import minidom
from time import sleep
import xmltodict
import json
import requests
from suds.client import Client
import simplejson

client_number = 1020004365
client_key = '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'


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
        for key, value in i:
            city[key] = key
        cities_arr.append(city)

    f = open('output.txt', 'w')
    simplejson.dump(cities_arr, f)
    f.close()
    return {'orig_resp': result, 'simple_list': cities_arr}


def get_service_cost(from_city,to_city,self_pickup,self_delivery):
    '''
    returns dict 
    orig_resp - object list (???)
    list - cities list that contains city properties

    '''


    url = "http://ws.dpd.ru/services/calculator2?wsdl"
    client = Client(url)
    req_data = {}
    auth = {'clientNumber': 1020004365,
            'clientKey': '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'}
    req_data['auth'] = auth

    pickup = {'cityName':from_city}
    req_data['pickup'] = pickup

    delivery = {'cityName':to_city}
    req_data['delivery'] = delivery

    req_data['selfPickup'] = self_pickup
    req_data['selfDelivery'] = self_delivery
    req_data['serviceCode'] = 'BZP, ECN'
    req_data['parcel'] = {'weight':from_city}


    




    result = client.service.getCitiesCashPay(request=req_data)

    cities_arr = []
    for i in result:
        city = {}
        for key, value in i:
            city[key] = key
        cities_arr.append(city)

    f = open('output.txt', 'w')
    simplejson.dump(cities_arr, f)
    f.close()
    return {'orig_resp': result, 'list': cities_arr}

