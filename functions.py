import csv
def match_tariffs(data, file_name, encoding):
    with open(file_name, 'r', newline = '', encoding = encoding) as file:
        reader = csv.DictReader(file, delimiter = ';')
        for i in reader:
            if i['tariff_name'] == data['tariffName']:

               return i['sdek_id'], i['pony_id'], i['another_id']