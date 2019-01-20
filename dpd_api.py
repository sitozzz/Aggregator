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
import datetime

client_number = 1020004365
client_key = '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'

f = open('dpd_cities.txt', 'r',encoding="utf8").read()
f = ast.literal_eval(f)

dpd_prefix = '[DPD] \n'

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
    #print("-------------------")
    #print(cityName)
    #print(f[0])
    cityProp = {'cityName':cityName}
    for city in f:
        if city['cityName'] == cityName:
            cityProp = {'cityName':cityName, "cityId": city['cityId']}
    #print(cityProp)
    #print("-------------------")
    return cityProp
             
    

def get_service_cost(req):
    
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
    req_data['serviceCode'] = 'ECN,CUR,NDY,PCL,DPI,DPE,ECU' #MXO,
    req_data['parcel'] = {'weight':weight,'length':length,'width':width,'height':height}

    output = []
    try:
        result = client.service.getServiceCostByParcels2(request=req_data)
        vrs = []
        for i in result:
            vr = {}
            for key in i:
                vr[key[0]] = key[1]
            vrs.append(vr)

        
        
        print(dpd_prefix)
        print(vrs)

        for i in vrs:
            ship_dt = str(datetime.datetime.now()).split(' ')[0]
            res_dt = str(datetime.datetime.now() + datetime.timedelta(days=i['days'])).split(' ')[0]
            output.append({
            'name': 'dpd',
            'price': i['cost'],
            'shippingDate': ship_dt,
            'receivingDate': res_dt,
            'tariffId': i['serviceCode']
            })
            
    except Exception as identifier:
        print(dpd_prefix)
        print(identifier)
        
        #return {'orig_resp': str(identifier) , 'list': str(identifier)}
        
    


    return output

def sobject_to_dict(obj, key_to_lower=False, json_serialize=True):
    """
    Converts a suds object to a dict.
    :param json_serialize: If set, changes date and time types to iso string.
    :param key_to_lower: If set, changes index key name to lower case.
    :param obj: suds object
    :return: dict object
    """
    import datetime

    if not hasattr(obj, '__keylist__'):
        if json_serialize and isinstance(obj, (datetime.datetime, datetime.time, datetime.date)):
            return obj.isoformat()
        else:
            return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if key_to_lower:
            field = field.lower()
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(sobject_to_dict(item, json_serialize=json_serialize))
        else:
            data[field] = sobject_to_dict(val, json_serialize=json_serialize)
    return data

def sobject_to_json(obj, key_to_lower=False):
    """
    Converts a suds object to json.
    :param obj: suds object
    :param key_to_lower: If set, changes index key name to lower case.
    :return: json object
    """
    import json
    data = sobject_to_dict(obj, key_to_lower=key_to_lower, json_serialize=True)
    f = open('dpd_terminals.json', 'w',encoding="utf8")
    json.dump(data, f,ensure_ascii=False)
    f.close()
    return json.dumps(data)

def get_terminals():
    
    url = "http://ws.dpd.ru/services/geography2?wsdl"
    client = Client(url)
    req_data = {}
    auth = {'clientNumber': 1020004365,
            'clientKey': '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'}
    req_data['auth'] = auth

    result = client.service.getParcelShops(request=req_data)
    print(type(result))
    result = sobject_to_json(result)
    print(type(result))

    

    print(type(result))
    cities_arr = []
    for i in result:
        city = {}
        #i = Client.dict(i)
        for key in i:
            city[key[0]] = key[1]
        cities_arr.append(city)
    f = open('dpd_terminals.txt', 'w',encoding="utf8")
    simplejson.dump(cities_arr, f,ensure_ascii=False)
    f.close()

# def get_terminals_by_city():
    
    

    

#     print(type(result))
#     cities_arr = []
#     for i in result:
#         city = {}
#         #i = Client.dict(i)
#         for key in i:
#             city[key[0]] = key[1]
#         cities_arr.append(city)
#     f = open('dpd_terminals.txt', 'w',encoding="utf8")
#     simplejson.dump(cities_arr, f,ensure_ascii=False)
#     f.close()
    
    
def make_order(data):
    
    url = "http://ws.dpd.ru/services/order2?wsdl"
    client = Client(url)
    req_data = {}
    auth = {'clientNumber': 1020004365,
            'clientKey': '04CD36DEDACCD77DB1424218BF57A57F6D82A12F'}
    

    req_data['auth'] = auth
    senderAddress = {
        'name' : 'Иванов Сергей Петрович',
        'terminalCode' : '032L',
        'countryName' : 'Россия',
        'city' : 'Екатеринбург',
        'street' : 'Есенина',
        'house' : 10,
        'contactPhone' : '79292155373',
        'contactFio' : 'Комаров Василий Дмитриевич'
    }
    
    header = {
        'datePickup' : '2019-01-16',
        #'payer' : 'sdf',
        'senderAddress' : senderAddress,
        'pickupTimePeriod' : '9-18',

        
    }
    req_data['header'] = header
    receiverAddress = {
        'name' : 'Иванов Иван Петрович',
        'terminalCode' : '045S',
        'countryName' : 'Россия',
        'city' : 'Екатеринбург',
        'street' : 'Есенина',
        'house' : 10,
        'contactPhone' : '79292155373',
        'contactFio' : 'Комаров Василий Дмитриевич'

    }
    order = {
        'orderNumberInternal' : '123456',
        'serviceCode' : 'DPE',
        'serviceVariant' : 'TT',
        'cargoNumPack' : 1,
        'cargoWeight' : 1,
        'cargoRegistered' : False,
        'cargoCategory' : 'Одежда',
        'receiverAddress' : receiverAddress,

    }
    req_data['order'] = order


    # try:
    result = client.service.createOrder(orders=req_data)
    print(result)
    # except Exception as identifier:
    #     print('DPD ERROR')
    #     return {'orig_resp': str(identifier) , 'list': str(identifier)}

#get_cities()
#get_service_cost('кемерово','екатеринбург',True,True,1,20,20,20)
#make_order()
#get_terminals()



