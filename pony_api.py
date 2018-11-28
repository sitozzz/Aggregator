import requests
from suds.client import Client


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
      print('EDIK TUT DLINA')
      print (length)
      width = req['goods'][0]['width']
      height = req['goods'][0]['height']
  else:
      length = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
      print('EDIK TUT DLINA')
      print (length)
      width = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
      height = round((int(req['goods'][0]['volume']) * 1000000)**(1/3))
  url = "https://svc-api.p2e.ru/UI_Service.svc?singleWsdl"
  client = Client(url)

  body = '''
  <?xml version="1.0" encoding="utf-8"?>
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
            <Mode>Express</Mode>
            <Sender>
              <Address>
                <Country>Россия</Country>
                <PostCode>127023</PostCode>
                <City>Москва</City>
                <StreetAddress>ул.Строителей, д.13</StreetAddress>
                </Address>
            </Sender>
            <Recipient>
              <Address>
                <Country>Россия</Country>
                <Region>Красноярcкий край</Region>
                <PostCode>660013</PostCode>
                <City>Красноярск</City>
                <StreetAddress>ул.Взлетная, д.1</StreetAddress>
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
                  <Length>'''+length+'''</Length>                <Width>300</Width>                <Height>200</Height>              </Dimentions>
                <Weight>800</Weight>              <Cost>10000</Cost>
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
    #return re
  print('result PONY')
  print(result)
  return result
