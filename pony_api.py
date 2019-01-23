import requests
from suds.client import Client
import xmltodict
import datetime

def get_service_cost(req):
     
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

  
  url = "https://svc-api.p2e.ru/UI_Service.svc?singleWsdl"
  client = Client(url)

  body = '''<?xml version="1.0" encoding="utf-8"?>
  <Request xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:type="OrderRequest">
    <Id>1</Id>  <Mode>Calculation</Mode>  <OrderList>
      <Order>      <ClientsNumber>kb48-12744</ClientsNumber>      <Payment>
          <Mode>Bill</Mode>
          <PaymentContract>
            <Number>70-989</Number>        </PaymentContract>
        </Payment>
        <ServiceList>
          <Service xsi:type="DeliveryService">
            <Id>1</Id>
            <Sender>
              <Address>
                <Country>Россия</Country>
                <City>'''+from_city+'''</City>
                <StreetAddress/>
                </Address>
            </Sender>
            <Recipient>
              <Address>
                <Country>Россия</Country>
                <Region/>
                <City>'''+to_city+'''</City>
                <StreetAddress/>
                </Address>
            </Recipient>
            <CargoList>
              <Cargo>
                <Id>1</Id>
                <Barcode>12345235</Barcode>
                <Description>Штучки</Description>
                <Packing>
                  <Type>Box</Type>
                </Packing>
                <Dimentions>
                  <Length>'''+length+'''</Length>                <Width>'''+width+'''</Width>                <Height>'''+height+'''</Height>              </Dimentions>
                <Weight>'''+str(int(float(weight)*1000))+'''</Weight>              <Cost>10000</Cost>
              </Cargo>
            </CargoList>
            <Unformalized>Доставка запчастей</Unformalized>
          </Service>
        </ServiceList>
      </Order>
    </OrderList>
  </Request>
  '''
  result = client.service.SubmitRequest('6f0ef6b3-e39e-40b2-85af-185bb5a73e62', body)
  # print(result)
  result=xmltodict.parse(result)

    #return re
  # print('result PONY')
  print(result['Response']['OrderList']['Order']['ServiceList']['Service']['Calculation']['DeliveryRateSet']['DeliveryRate'])
  result=result['Response']['OrderList']['Order']['ServiceList']['Service']['Calculation']['DeliveryRateSet']['DeliveryRate']
  #return result
  if req['deliveryType']['deliveryFrom'] == 'storage':
        self_pickup = True
  else:
        self_pickup = False
    
  if req['deliveryType']['deliveryTo'] == 'storage':
        self_delivery = True
  else:
        self_delivery = False
  for i in range(len(result)):
    try:
        result[i]=dict(result[i])
        print (result[i])
        if result[i]['DeliveryMethod'] == 'Самовывоз':
            print(result[i]['Mode']+result[i]['Sum']+result[i]['Description'])
    except IndexError:
        break
  pony_output=[]
  ship_date = datetime.datetime.now()
  
  for i in result:
    res_date = str(datetime.datetime.now() + datetime.timedelta(days=int(i['MaxTerm']))).split(' ')[0]
    if self_pickup == True:
      if i['DeliveryMethod'] == 'Самовывоз':
        pony_output.append({
          'name': 'PonyExpress',
          'price': round(float(i['Sum'])+float(i['VAT']),2),
          'shippingDate': str(ship_date).split(' ')[0],
          'receivingDate': res_date,
          'tariffId': i['Mode']
          })
    else:
      if i['DeliveryMethod'] == 'Курьерская доставка':
        pony_output.append({
          'name': 'PonyExpress',
          'price': round(float(i['Sum'])+float(i['VAT']),2),
          'shippingDate': str(ship_date).split(' ')[0],
          'receivingDate': res_date,
          'tariffId': i['Mode']
          })
  return pony_output     
            
