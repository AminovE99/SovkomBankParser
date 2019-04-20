import json
import re

import requests
from bs4 import BeautifulSoup

from dadata import get_useful_info_from_dadata
from database import insert_words_list

'''

give_post_to_extra_service - эта функция находит по одной строке информацию в url /extra
give_get_to_service - Эта функция находит на главной странице всю информацию по одной строке
'''

#
# def give_post_to_extra_service(address, info):
#     macroRegionId = "1" + str(int(info['okato']) // 1000000000) + "000000000"
#     regionId = "1" + str(int(info['okato']) // 1000000) + "000000"
#     settlementId = "1" + str(int(info['okato']) // 1000) + "000"
#     url = "https://extra.egrp365.ru/api/extra/index.php"
#     data = {
#         "macroRegionId": macroRegionId,
#         "regionId": regionId,
#         "settlementId": settlementId,
#         "street": info['street'],
#         "house": info['house_num'],
#         "structure": None,
#         "building": info['building_num'],
#         "apartment": info['flat_num'],
#         "method": "searchByAddress"
#     }
#     headers = {'user-agent': 'Mozilla/5.0'}
#     return requests.post(url, data=data, headers=headers)


'''
Респ Коми, г Печора, Печорский пр-кт, д 116, кв 51
?street={info['street']}&house={info['house_num']}&building={info['building_num']}&mregion={info['region']}&area=null&city={info['city']}&apartment={info['flat_num']}&link=page&fiasid={info['fias_id']}

'''


def give_get_to_service(info):
    url = f"https://egrp365.ru/list4.php"
    data = {
        "street": info['street'],
        "house": info['house_num'],
        "mregion": info['region'],
        "building": info['building_num'],
        "city": info['city'],
        "apartment": info['flat_num'],
        "area": None,
        "link": "page",
        "fiasid": info['fias_id']
    }
    headers = {'user-agent': 'Mozilla/5.0'}
    return requests.get(url, data, headers=headers)


def get_space_and_floor_and_metres(link):
    soup = BeautifulSoup(''.join(requests.get(link).text))
    info = soup.find('div', {"id": "information_about_object"}).contents
    info = str(info)
    floor = None
    place = None
    try:
        place = info.split('Описание —')[1].split("<br")  # квартира
    except IndexError:
        print('Земельный участок')

    try:
        floor = info.split('Этаж —')[1].split("<br")[0]  # этаж
    except IndexError:
        print('этажа нет')
    metres = info.split('Площадь —')[1].split("<br")[0]
    info_dict = {'place': place, 'floor': floor, 'metres': metres}
    print("info_dict" + str(info_dict))
    return info_dict


def one_str_address(address):
    info = get_useful_info_from_dadata(address)
    if info == -1:
        return -1
    resp = give_get_to_service(info).text
    element = json.loads(resp)
    if element['error'] == 1:
        print("Информация не найдена")
        return -1
    egrp = element['data'].split('reestr?egrp=')[1].split('\'')[0]  # Хардкод! Поменять на регулярки
    link = 'https://egrp365.ru/reestr?egrp=' + egrp
    info_dict = get_space_and_floor_and_metres(link)
    insert_words_list(kadastr_num=egrp,
                      address=address,
                      link_of_kadastr_num=link,
                      floor=info_dict['floor'],
                      json=json.dumps(element),
                      square=info_dict['metres'],
                      lat=info['lat'],
                      long=info['lon']
                      )







if __name__ == '__main__':
    print("1. Написать адрес одной строкой\n"
          "2. Расширенный поиск")
    choice = input("Введите желаемое действие: ")
    if choice == '1':
        address = input("Напишите адрес, где расположен дом: ")
        one_str_address(address)
    if choice == '2': # Лучше не использовать else, потому что функционал может дополниться
        region = input("Регион: ")
        city = input("Город: ")
        street = input("Улица: ")
        house = input("Номер дома: ")
        address_block = input("корпус(необяз): ")
        flat = input('Квартира: ')
        if address_block is not None:
            address = f"{region},г.{city},{street},д.{house},корп.{address_block},кв.{flat}"
        else:
            address = f"{region},г.{city},{street},д.{house},кв.{flat}"
        print(f"Адрес для валидации: {address}")
        one_str_address(address)