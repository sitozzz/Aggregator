import requests
import csv

token = '84327.pjpqbddd'
url = 'http://api.boxberry.de/json.php'

file_zips = 'list_zips_boxberry.csv'
file_cities = 'list_cities_boxberry.csv'
file_points_for_parcels = 'list_points_for_parcels_boxberry.csv'
file_points = 'list_points_boxberry.csv'

def get_json(url, data = None):
    response = requests.get(url, params = data)
    print(response.url)
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
    
    :param code_city: (optional) код города в boxberry, без указания кода вернет все пункты выдачи.
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
    
    :param point_code: код пункта выдачи заказов.
    :param photo: (optional) получить изображения.
    :return: массив значений."""
    return get_json(url, {
        'token'  : token,
        'method' : 'PointsDescription',
        'code'   : point_code,
        'photo'  : photo
    })

def get_point_by_zip(zip_code):
    """Получить код ближайшего пункта выдачи заказов по почтовому индексу.

    :param zip_code: почтовый код.
    :return: код пункта выдачи заказов."""
    return get_json(url, {
        'token'  : token,
        'method' : 'PointsByPostCode',
        'zip'    : zip_code,
    })['Code']

def zip_check(zip_code):
    """Проверить возможность курьерской доставки для заданного индекса.
    
    :param zip_code: почтовый код.
    :return: True если возможно, False нет."""
    return get_json(url, {
        'token'  : token,
        'method' : 'ZipCheck',
        'Zip'    : zip_code
    })[0]['ExpressDelivery']

def find_city_in_data(name_sity, list_cities):
    """Поиск в листе словарей города с заданым именем.
    
    :param name_city: название города.
    :param list_cities: список словарей городов.
    :return: словарь для заданного города."""
    for i in list_cities:
        if i['Name'] == name_sity:
            return i

def find_list_points_for_city(code_city, list_points):
    """Поиск всех пунктов выдачи заказов в заданном городе.
    
    :param code_city: код города в boxberry.
    :param list_points: список словарей пунктов выдачи заказов для всех городов.
    :return: список словарей пунктов выдачи заказов для заданного города."""
    points = []

    for i in list_points:
        if i['CityCode'] == code_city:
            points.append(i)

    return points

def find_list_points_for_parcels_for_city(name_city, list_points):
    """Поиск всех пунктов приема в заданном городе.
    
    :param name_city: название города.
    :param list_points: список словарей пунктов приема для всех городов.
    :return: список словарей пунктов приема для заданного города."""
    points = []

    for i in list_points:
        if i['City'] == name_city:
            points.append(i)

    return points

def find_zips_for_city(name_city, zips):
    """Поиск всех почтовых индексов для заданого города.
    
    :param name_city: название города.
    :param zips: список словарей почтовых индексов для всех городов.
    :return: список словарей почтовых индексов для заданного города."""
    zips_in_city = []

    for i in zips:
        if i['City'] == name_city:
            zips_in_city.append(i)

    return zips_in_city

def check_courier_delivery(city):
    """Проверка возможности доставки курьером на основе данных о городе.
    
    :param city: словарь данных о городе.
    :return: True возможна доставка курьером, False нет."""
    return city['CourierDelivery']

def filter_by_point(points, weight, volume):
    """Отфильтровать точки по весу и объему.
    
    :param points: пункты выдачи заказов.
    :param weight: вес посылки.
    :param volume: объем посылки.
    :return: отфильтрованный список пунктов выдачи заказов."""
    filtered_points = []

    for i in points:
        if int(i['LoadLimit']) >= weight and float(i['VolumeLimit']) >= volume:
            filtered_points.append(i)

    return filtered_points

def write_csv(data, file_name, columns, encoding = 'utf-8'):
    """Записать лист словарей в файл ('*.csv').
    
    :param data: лист словарей.
    :param file_name: имя файла в который произведется запись.
    :param columns: заголовки колонок в виде списка строк.
    :param encoding: (optional) кодировка по умолчанию ('utf-8').
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
    
    :param file_name: имя файла из которого считываются данные.
    :param name_city: имя города, которое необходимо найти.
    :param encoding: (optional) кодировка по умолчанию ('utf-8').
    :return: словарь данных, в случае если город не найден None."""
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        reader = csv.DictReader(file, delimiter = ';')
        try:
            for i in reader:
                if i['Name'] == name_city:
                    return i
        except csv.Error:
            return None

def take_points_for_parcels_from_csv(file_name, name_city, encoding = 'utf-8'):
    """Получить пункты приема в заданном городе из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.
    :param name_city: имя города в котором необходимо найти пункты приема.
    :param encoding: (optional) кодировка по умолчанию ('utf-8').
    :return: лист словарей данных, в случае если город не найден пустой массив
        В случае ошибки чтения None."""
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        points = []
        reader = csv.DictReader(file, delimiter = ';')
        try:
            for i in reader:
                if i['City'] == name_city:
                    points.append(i)
        except csv.Error:
            return None
        
        return points

def take_points_of_issue_orders(file_name, code_city, encoding = 'utf-8'):
    """Получить пункты приема в заданном городе из файла ('*.csv').
    
    :param file_name: имя файла из которого считываются данные.
    :param code_city: код города в boxberry.
    :param encoding: (optional) кодировка по умолчанию ('utf-8').
    :return: лист словарей данных, в случае если город не найден пустой массив
        В случае ошибки чтения None."""
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        points = []
        reader = csv.DictReader(file, delimiter = ';')
        try:
            for i in reader:
                if i['CityCode'] == code_city:
                    points.append(i)
        except csv.Error:
            print('Error')
            return None
        
        return points

def get_delivery_costs(sender_city, recipient_city, weight, zip_code, advanced_sending_options = None):
    """Расчет стоимости доставки посылки до ПВЗ, возможен расчет с учетом курьерской доставки.
    
    :param sender_city: str, город отправителя.
    :param recipient_city: str, город получателя.
    :param weight: вес посылки в (граммах).
    :param zip_code: почтовый индекс для курьерской доставки.
    :param advanced_sending_options: (optional) Dictionary,
        дополнительные парамеры отправки('height', 'width', 'depth') в (см.).
    :return costs: стоимость доставки, time: срок доставки (дней).
    :rtype: str, str."""
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
        'targetstart' : sender_city,
        'height'      : height,
        'width'       : width,
        'depth'       : depth,
        'zip'         : zip_code
    })

    print(delivery_costs)

    return delivery_costs['price'], delivery_costs['delivery_period']


def get_name_city(name):
    """Получить название города из строки запроса.
    
    :param name: строка включающая название города.
    :return: название города."""
    name_city = name.split(',')

    return name_city[0]

def data_loading():
    """Загрузка данных в ('*.csv') файлы."""
    list_cities = get_list_cities()
    write_csv(list_cities, file_cities, list_cities[0].keys())
    list_points = get_list_points()
    write_csv(list_points, file_points, list_points[0].keys())
    list_zips = get_list_zips()
    write_csv(list_zips, file_zips, list_zips[0].keys())
    list_points_for_parcels = get_points_for_parcels()
    write_csv(list_points_for_parcels, file_points_for_parcels, list_points_for_parcels[0].keys())

def get_data(request):
    """Получить цену за доставку и кол-во дней доставки.
    
    :return: словарь данных, в случае если получить данные невозможно возвращается пустой словарь."""
    sender_city = get_name_city(request['city1']['name'])
    recipient_city = get_name_city(request['city2']['name'])

    try:
        weight = float(request['goods'][0]['weight'])
        height = float(request['goods'][0]['height'])
        width = float(request['goods'][0]['width'])
        depth = float(request['goods'][0]['length'])
    except:
        height = 0
        width = 0
        depth = 0

    volume = (height * width * depth) / 1000000
    if height + width + depth > 250:
        return {}
    if weight > 31:
        return {}
    
    city_a = take_city_from_csv(file_cities, sender_city)
    city_b = take_city_from_csv(file_cities, recipient_city)
    points_for_parcels = take_points_for_parcels_from_csv(file_points_for_parcels, city_a['Name'])
    points_of_issue_orders = take_points_of_issue_orders(file_points, city_b['Code'])
    points_of_issue_orders = filter_by_point(points_of_issue_orders, weight, volume)
    price, period = get_delivery_costs(
        points_for_parcels[0]['Code'], 
        points_of_issue_orders[0]['Code'], 
        weight * 1000, 
        0, 
        {'height' : height, 'width' : width, 'depth' : depth})
    
    return {
        'price'  : price,
        'period' : period
    }