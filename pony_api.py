import requests
from suds.client import Client

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
          <Mode>Express</Mode>
          <Sender>
            <Address>
              <Country>Россия</Country>
              <PostCode>127023</PostCode>
              <City>Москва</City>
              <StreetAddress>ул.Строителей, д.13</StreetAddress>
              </Address>
            <Company>
              <Name>ОАО "Компания"</Name>
            </Company>
            <PersonList>
              <Person>
                <Name>Петров Игорь Иванович</Name>
                <PhoneList>
                  <string>+7 495 342-3422</string>
                  <string>12-44</string>
                </PhoneList>              </Person>
              <Person>
                <Name>Иванов Семен</Name>
                <PhoneList>
                  <string>+7 910 456-7895</string>
                </PhoneList>              </Person>
            </PersonList>
          </Sender>
          <Recipient>
            <Address>
              <Country>Россия</Country>
              <Region>Красноярcкий край</Region>
              <PostCode>660013</PostCode>
              <City>Красноярск</City>
              <StreetAddress>ул.Взлетная, д.1</StreetAddress>
              </Address>
            <Company>
              <Name>ОАО "Самолет"</Name>
            </Company>
            <PersonList>
              <Person>
                <Name>Шпак Геннадий Семенович</Name>
                <PhoneList>
                  <string>+3912 34-23-12</string>
                  <string>11-4</string>
                </PhoneList>              </Person>
            </PersonList>
            <Unformalized>Или любому другому лицу в компании</Unformalized>
          </Recipient>
          <CargoList>
            <Cargo>
              <Id>1</Id>
              <Barcode>12345234</Barcode>
              <Description>Пимпачки и помпочки</Description>
              <Packing>
                <Type>Box</Type>
              </Packing>
              <Dimentions>
                <Length>350</Length>                <Width>500</Width>                <Height>300</Height>              </Dimentions>
              <Weight>1400</Weight>              <Cost>500</Cost>
            </Cargo>
            <Cargo>
              <Id>2</Id>
              <Barcode>12345235</Barcode>
              <Description>Штучки</Description>
              <Packing>
                <Type>Box</Type>
              </Packing>
              <Dimentions>
                <Length>250</Length>                <Width>300</Width>                <Height>200</Height>              </Dimentions>
              <Weight>800</Weight>              <Cost>10000</Cost>
            </Cargo>
          </CargoList>
          <ItemList>
            <Item>
              <Id>1</Id>
              <CargoId>1</CargoId>
              <Barcode>art2341667</Barcode>
              <Description>Пимпачка</Description>
              <Weight>50</Weight>              <Cost>50</Cost>
              <Count>100</Count>
            </Item>
            <Item>
              <Id>2</Id>
              <CargoId>1</CargoId>
              <Barcode>art2341668</Barcode>
              <Description>Помпочка</Description>
              <Weight>140</Weight>              <Cost>66</Cost>
              <Count>50</Count>
            </Item>
            <Item>
              <Id>3</Id>
              <CargoId>2</CargoId>
              <Barcode>art2342340</Barcode>
              <Description>Штучка</Description>
              <Weight>8</Weight>              <Cost>100</Cost>
              <Count>11</Count>
            </Item>
          </ItemList>
          <Unformalized>Доставка запчастей</Unformalized>
        </Service>
      </ServiceList>
    </Order>
  </OrderList>
</Request>
'''


result = client.service.SubmitRequest('6f0ef6b3-e39e-40b2-85af-185bb5a73e62', body)

print(result)
