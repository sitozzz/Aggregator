import requests
import csv
import json
import uuid
import datetime

token = '84327.pjpqbddd'
url = 'http://api.boxberry.de/json.php'

file_zips = 'list_zips_boxberry.csv'
file_cities = 'list_cities_boxberry.csv'
file_points_for_parcels = 'list_points_for_parcels_boxberry.csv'
file_points = 'list_points_boxberry.csv'

def get_json(url, data = None):
    response = requests.get(url, params = data)
    return response.json()

#достаточно обновления 1 раз в день
def get_list_cities():
    """Получить список городов, в которые осуществляется доставка.
    
    :return: list of Dictionary."""
    return get_json(url, {
        'token'  : token,
        'method' : 'ListCitiesFull'
    })

#достаточно обновления 1 раз в день
def get_list_zips():
    """Получить список почтовых индексов, для которых возможна доставка.
    
    :return: list of Dictionary."""
    return get_json(url, {
        'token'  : token,
        'method' : 'ListZips'
    })

#достаточно обновления 1 раз в час
def get_list_points():
    """Получить все точки выдачи заказов.
    
    :return: list of Dictionary."""
    return get_json(url, {
        'token'   : token,
        'method'  : 'ListPoints',
        'prepaid' : '1'
    })

def get_list_points_for_city(code_city = ''):
    """Получить коды всех пунктов выдачи заказов для города.
    
    :param code_city: (optional) код города в boxberry, без указания кода вернет все пункты выдачи.\n
    :return: list of Dictionary."""
    return get_json(url, {
        'token'   : token,
        'method'  : 'ListPointsShort',
        'CityCode' : code_city
    })

#достаточно обновления 1 раз в час
def get_points_for_parcels():
    """Получить список точек приёма посылок.
    
    :return: list of Dictionary."""
    return get_json(url, {
        'token'  : token,
        'method' : 'PointsForParcels'
    })

def get_description_point(point_code, photo = False):
    """Получить полное описание пункта выдачи заказов.
    
    :param point_code: код пункта выдачи заказов.\n
    :param photo: (optional) получить изображения.\n
    :return: list."""
    return get_json(url, {
        'token'  : token,
        'method' : 'PointsDescription',
        'code'   : point_code,
        'photo'  : photo
    })

def get_point_by_zip(zip_code):
    """Получить код ближайшего пункта выдачи заказов по почтовому индексу.

    :param zip_code: почтовый код.\n
    :return: код пункта выдачи заказов или None в случае ошибки запроса."""
    try:
        return get_json(url, {
            'token'  : token,
            'method' : 'PointsByPostCode',
            'zip'    : zip_code,
        })['Code']
    except:
        return None

def zip_check(zip_code):
    """Проверить возможность курьерской доставки для заданного индекса.
    
    :param zip_code: почтовый код.\n
    :return: True если возможно, False нет."""
    try:
        return get_json(url, {
            'token'  : token,
            'method' : 'ZipCheck',
            'Zip'    : zip_code
        })[0]['ExpressDelivery']
    except:
        return False

def find_city_in_data(name_sity, list_cities):
    """Поиск в листе словарей города с заданым именем.
    
    :param name_city: название города.\n
    :param list_cities: список словарей городов.\n
    :return: Dictionary для заданного города или None если город не найден."""
    for i in list_cities:
        if i['Name'] == name_sity:
            return i

    return None

def find_elements(value, list_elements, name_element):
    elements = []

    for i in list_elements:
        if i[name_element] == value:
            elements.append(i)

    return elements

def find_list_points_for_city(code_city, list_points):
    """Поиск всех пунктов выдачи заказов в заданном городе.
    
    :param code_city: код города в boxberry.\n
    :param list_points: список словарей пунктов выдачи заказов для всех городов.\n
    :return: list of Dictionary пунктов выдачи заказов для заданного города."""
    return find_elements(code_city, list_points, 'CityCode')

def find_list_points_for_parcels_for_city(name_city, list_points):
    """Поиск всех пунктов приема в заданном городе.
    
    :param name_city: название города.\n
    :param list_points: список словарей пунктов приема для всех городов.\n
    :return: list of Dictionary пунктов приема для заданного города."""
    return find_elements(name_city, list_points, 'City')

def find_zips_for_city(name_city, zips):
    """Поиск всех почтовых индексов для заданого города.
    
    :param name_city: название города.\n
    :param zips: список словарей почтовых индексов для всех городов.\n
    :return: list of Dictionary почтовых индексов для заданного города."""
    return find_elements(name_city, zips, 'City')

def check_courier_delivery(city):
    """Проверка возможности доставки курьером на основе данных о городе.
    
    :param city: словарь данных о городе.\n
    :return: True возможна доставка курьером, False нет."""
    return city['CourierDelivery']

def filter_by_point(points, weight, volume):
    """Отфильтровать точки по весу и объему.
    
    :param points: пункты выдачи заказов.\n
    :param weight: вес посылки.\n
    :param volume: объем посылки.\n
    :return: отфильтрованный список пунктов выдачи заказов."""
    filtered_points = []

    for i in points:
        if int(i['LoadLimit']) >= weight and float(i['VolumeLimit']) >= volume:
            filtered_points.append(i)

    return filtered_points

def write_csv(data, file_name, columns, encoding = 'utf-8'):
    """Записать list of Dictionary в файл ('*.csv').
    
    :param data: list of Dictionary.\n
    :param file_name: имя файла в который произведется запись.\n
    :param columns: заголовки колонок в виде списка строк.\n
    :param encoding: (optional) кодировка по умолчанию ('utf-8').\n
    :return: True если запись прошла успешо, False нет."""
    with open(file_name, 'w', newline = '', encoding = encoding) as file:
        writer = csv.DictWriter(file, delimiter = ';', fieldnames = columns)
        try:
            writer.writeheader()
            writer.writerows(data)
        except csv.Error:
            return False

    return True

def take_city_from_csv(file_name, name_city, encoding = 'utf-8'):
    """Получить словарь данных о городе по имени годода из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.\n
    :param name_city: имя города, которое необходимо найти.\n
    :param encoding: (optional) кодировка по умолчанию ('utf-8').\n
    :return: словарь данных, в случае если город не найден None."""
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        reader = csv.DictReader(file, delimiter = ';')
        try:
            for i in reader:
                if i['Name'] == name_city:
                    return i
        except csv.Error:
            return None

        return None

def take_from_csv(file_name, value, name_element, encoding = 'utf-8'):
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        elements = []
        reader = csv.DictReader(file, delimiter = ';')
        try:
            for i in reader:
                if i[name_element] == value:
                    elements.append(i)
        except csv.Error:
            return None
        
        return elements

def take_points_for_parcels_from_csv(file_name, name_city, encoding = 'utf-8'):
    """Получить пункты приема в заданном городе из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.\n
    :param name_city: имя города в котором необходимо найти пункты приема.\n
    :param encoding: (optional) кодировка по умолчанию ('utf-8').\n
    :return: list of Dictionary, в случае если город не найден пустой массив.
    В случае ошибки чтения None."""
    return take_from_csv(file_name, name_city, 'City', encoding)

def take_points_of_issue_orders(file_name, code_city, encoding = 'utf-8'):
    """Получить пункты приема в заданном городе из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.\n
    :param code_city: код города в boxberry.\n
    :param encoding: (optional) кодировка по умолчанию ('utf-8').\n
    :return: list of Dictionary, в случае если город не найден пустой массив.
    В случае ошибки чтения None."""
    return take_from_csv(file_name, code_city, 'CityCode', encoding)

def take_zips_for_city(file_name, name_city, encoding = 'utf-8'):
    """Получить почтовые индексы в заданном городе из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.\n
    :param name_city: имя города в котором необходимо найти почтовые индексы.\n
    :param encoding: (optional) кодировка по умолчанию ('utf-8').\n
    :return: list of Dictionary, в случае если город не найден пустой массив.
    В случае ошибки чтения None."""
    return take_from_csv(file_name, name_city, 'City', encoding)

def get_delivery_costs(sender_city, recipient_city, ordersum, weight, zip_code, advanced_sending_options):
    """Расчет стоимости доставки посылки до ПВЗ, возможен расчет с учетом курьерской доставки.
    
    :param sender_city: город отправителя.\n
    :param recipient_city: город получателя.\n
    :param ordersum: заявленная стоимость ('руб.').\n
    :param weight: вес посылки в (граммах).\n
    :param zip_code: почтовый индекс для курьерской доставки.\n
    :param advanced_sending_options: (optional) Dictionary,\n
    дополнительные парамеры отправки('height', 'width', 'depth') в (см.).\n
    :return costs: стоимость доставки, time: срок доставки (дней)."""
    try:
        height = advanced_sending_options['height']
        width = advanced_sending_options['width']
        depth = advanced_sending_options['depth']
    except:
        height = 0
        width = 0
        depth = 0

    delivery_costs = get_json(url, {
        'token'       : token,
        'method'      : 'DeliveryCosts',
        'weight'      : weight,
        'target'      : recipient_city,
        'ordersum'    : ordersum,
        'targetstart' : sender_city,
        'height'      : height,
        'width'       : width,
        'depth'       : depth,
        'zip'         : zip_code
    })

    return delivery_costs['price'], delivery_costs['delivery_period']


def get_name_city(name):
    """Получить название города из строки запроса.
    
    :param name: строка включающая название города.\n
    :return: название города."""
    name_city = name.split(',')

    return name_city[0]

def data_loading():
    """Загрузка данных в ('*.csv') файлы."""
    list_cities = get_list_cities()
    write_csv(list_cities, file_cities, list_cities[0].keys())
    list_points_for_parcels = get_points_for_parcels()
    write_csv(list_points_for_parcels, file_points_for_parcels, list_points_for_parcels[0].keys())
    list_points = get_list_points()
    write_csv(list_points, file_points, list_points[0].keys())
    list_zips = get_list_zips()
    write_csv(list_zips, file_zips, list_zips[0].keys())

def calculate_boxberry(sender_city, recipient_city, advanced_sending_options, ordersum = 0, zip_code = 0):
    """Получить данные о доставке."""
    try:
        weight = float(advanced_sending_options['weight'])
    except:
        weight = 0

    try:
        height = float(advanced_sending_options['height'])
        width = float(advanced_sending_options['width'])
        depth = float(advanced_sending_options['length'])
    except:
        height = 0
        width = 0
        depth = 0

    if height == 0 and width == 0 and depth == 0:
        try:
            volume = float(advanced_sending_options['volume'])
            a = (volume ** (1 / 3)) * 100
            height = a
            width = a
            depth = a
        except:
            volume = 0
    else:
        volume = (height * width * depth) / 1000000

    if height > 120 or width > 120 or depth > 120:
        return []
    if height + width + depth > 250:
        return []
    if weight > 31:
        return []
    
    city_a = take_city_from_csv(file_cities, sender_city)
    city_b = take_city_from_csv(file_cities, recipient_city)

    if city_a == None or city_b == None:
        return []

    points_for_parcels = take_points_for_parcels_from_csv(file_points_for_parcels, city_a['Name'])

    if len(points_for_parcels) == 0:
        return []

    points_of_issue_orders = take_points_of_issue_orders(file_points, city_b['Code'])
    points_of_issue_orders = filter_by_point(points_of_issue_orders, weight, volume)

    if len(points_of_issue_orders) == 0:
        return []

    if zip_code != 0:
        if zip_code == 1:
            zips_for_city = take_zips_for_city(file_zips, recipient_city)
            zip_code = zips_for_city[0]['Zip']
        elif not zip_check(zip_code):
            zip_code = 0
        
    price, period = get_delivery_costs(
        points_for_parcels[0]['Code'], 
        points_of_issue_orders[0]['Code'], 
        ordersum, 
        weight * 1000, 
        zip_code, 
        {
            'height' : height, 
            'width' : width, 
            'depth' : depth
        })

    if zip_code == 0:
        reception_points = points_of_issue_orders
    else:
        reception_points = zips_for_city

    shipping_date = str(datetime.datetime.now()).split(' ')[0]
    receiving_date = str(datetime.datetime.now() + datetime.timedelta(days = period)).split(' ')[0]
    
    return [{
        'name'              : 'boxberry',
        'price'             : price,
        'receivingDate'     : receiving_date,
        'shippingDate'      : shipping_date,
        'shippingPoints'    : points_for_parcels,
        'receptionPoints'   : reception_points
    }]

def get_data_boxberry(request):
    if request['deliveryType']['deliveryFrom'] == 'door':
        return []
    
    sender_city = get_name_city(request['city1']['name'])
    recipient_city = get_name_city(request['city2']['name'])
    zip_code = 0

    if request['deliveryType']['deliveryTo'] == 'door':
        zip_code = 1

    return calculate_boxberry(sender_city, recipient_city, request['goods'][0], zip_code = zip_code)

def send_request(data = None):
    return requests.post(url, data = data)

def parsel_check(order_tracking_code):
    """Получить ссылку на файл печати этикеток.
    
    :param order_tracking_code: код отслеживания заказа.\n
    :return: ссылка на файл или None в случае ошибки запроса."""
    try:
        return get_json(url, {
            'token'     : token,
            'method'    : 'ParselCheck',
            'ImId'      : order_tracking_code
        })
    except:
        return None

def get_list_statuses(order_tracking_code):
    """Получить информацию о статусах посылки.
    
    :param order_tracking_code: код отслеживания заказа.\n
    :return: array статусов по данному заказу или None в случае ошибки запроса."""
    try:
        return get_json(url, {
            'token'     : token,
            'method'    : 'ListStatuses',
            'ImId'      : order_tracking_code
        })
    except:
        return None

def get_list_statuses_full(order_tracking_code):
    """Получить полную информацию о статусах посылки.
    
    :param order_tracking_code: код отслеживания заказа.\n
    :return: list of Dictionary данных по заказу или None в случае ошибки запроса."""
    try:
        return get_json(url, {
            'token'     : token,
            'method'    : 'ListStatusesFull',
            'ImId'      : order_tracking_code
        })
    except:
        return None

def get_list_services(order_tracking_code):
    """Получить перечень и стоимость оказанных услуг по отправлению.
    
    :param order_tracking_code: код отслеживания заказа.\n
    :return: array статусов по данному заказу или None в случае ошибки запроса."""
    try:
        return get_json(url, {
            'token'     : token,
            'method'    : 'ListServices',
            'ImId'      : order_tracking_code
        })
    except:
        return None

def parsel_delete(order_tracking_code):
    """Удалить посылку, но только в том случае, если она не была проведена в акте.
    
    :param order_tracking_code: код отслеживания заказа.\n
    :return: True в случае успешного удаления, False нет."""
    try:
        return get_json(url, {
            'token'     : token,
            'method'    : 'ParselDel',
            'ImId'      : order_tracking_code
        })['text'] == 'ok'
    except:
        return False

def create_parsel(data):
    """Создание/обновление посылки в личном кабинете.
    
    :param data: сформированные данные для создания заказа.\n
    :return: словарь данных."""
    return send_request({
        'token'     : token,
        'method'    : 'ParselCreate',
        'sdata'     : json.dumps(data)
    }).json()

def get_data_for_delivery_to_door(type_of_delivery, sender, recipient, weights):
    """Создание словаря данных для формирования заказа до двери."""
    customer = {
        'fio'           : recipient['name'],
        'phone'         : recipient['phone']
    }

    if 'email' in recipient:
        customer.update({
            'email' : recipient['email']
        })

    return {
        'order_id'          : uuid.uuid4().hex[:30],
        'price'             : '0',
        'payment_sum'       : '0',
        'delivery_sum'      : '0',
        'vid'               : type_of_delivery,
        'shop'              : {
            'name'          : recipient['code'],
            'name1'         : sender['code']
        },
        'customer'          : customer,
        'weights'           : weights
    }

def get_data_for_delivery_to_warehouse(type_of_delivery, sender, recipient, weights):
    """Создание словаря данных для формирования заказа до склада."""
    address = ', '.join([str(recipient['street']), str(recipient['flat']), str(recipient['house'])])
    customer = {
        'fio'           : recipient['name'],
        'phone'         : recipient['phone']
    }
    kurdost = {
        'index'         : recipient['zip'],
        'citi'          : recipient['nameCity'],
        'addressp'      : address
    }

    if 'email' in recipient:
        customer.update({
            'email' : recipient['email']
        })

    if 'coment' in recipient:
        kurdost.update({
            'coment' : recipient['coment']
        })

    return {
        'order_id'          : uuid.uuid4().hex[:30],
        'price'             : '0',
        'payment_sum'       : '0',
        'delivery_sum'      : '0',
        'vid'               : type_of_delivery,
        'shop'              : {
            'name1'         : sender['code']
        },
        'customer'          : customer,
        'kurdost'           : kurdost,
        'weights'           : weights
    }

def get_weights(package):
    try:
        weight = float(package['weight']) * 1000
    except:
        return None

    weights = {
        'weight' : weight
    }

    name_key = ['weight2', 'weight3', 'weight4', 'weight5']

    for i in name_key:
        if i in package and package[i] != '':
            try:
                weight = float(package[i]) * 1000
            except:
                return weights

            weights.update({
                i : float(weight)
            })
        else:
            return weights

def set_booking(request):
    weights = get_weights(request['package'])
    if weights == None:
        return {}

    if 'code' in request['reciever']:
        type_of_delivery = 1
        data = get_data_for_delivery_to_door(
            type_of_delivery, 
            request['sender'], 
            request['reciever'], 
            weights
        )
    elif 'zip' in request['reciever']:
        type_of_delivery = 2
        data = get_data_for_delivery_to_warehouse(
            type_of_delivery, 
            request['sender'], 
            request['reciever'], 
            weights
        )
    else:
        return {}

    return create_parsel(data)