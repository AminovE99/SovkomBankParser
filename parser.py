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


def give_post_to_extra_service(address, info):
    macroRegionId = "1" + str(int(info['okato']) // 1000000000) + "000000000"
    regionId = "1" + str(int(info['okato']) // 1000000) + "000000"
    settlementId = "1" + str(int(info['okato']) // 1000) + "000"
    url = "https://extra.egrp365.ru/api/extra/index.php"
    data = {
        "macroRegionId": macroRegionId,
        "regionId": regionId,
        "settlementId": settlementId,
        "street": info['street'],
        "house": info['house_num'],
        "structure": None,
        "building": info['building_num'],
        "apartment": info['flat_num'],
        "method": "searchByAddress"
    }
    headers = {'user-agent': 'Mozilla/5.0'}
    return requests.post(url, data=data, headers=headers)


def give_get_to_service(info):
    url = "https://egrp365.ru/list4.php"
    data = {
        "street": info['street'],
        "house": info['house_num'],
        "mregion": info['region'],
        "building": info['building_num'],
        "city": info['city'],
        "apartment": info['flat_num'],
        "area": None,
        "link": "page",
        "fias_id": info['fias_id']
    }
    headers = {'user-agent': 'Mozilla/5.0'}
    return requests.get(url, data=data)


def get_space_and_floor_and_metres(link):
    soup = BeautifulSoup(''.join(requests.get(link).text))
    info = soup.find('div', {"id": "information_about_object"}).contents
    info = str(info)
    floor = None
    place = info.split('Описание —')[1].split("<br")[0]  # квартира
    try:
        floor = info.split('Этаж —')[1].split("<br")[0]  # этаж
    except IndexError:
        print('этажа нет')
    metres = info.split('Площадь —')[1].split("<br")[0]
    info_dict = {'place': place, 'floor': floor, 'metres': metres}
    print("info_dict" + str(info_dict))
    return info_dict


if __name__ == '__main__':
    address = input("Напишите адрес, где расположен дом: ")
    info = get_useful_info_from_dadata(address)
    resp = give_post_to_extra_service(address, info).text
    resp2 = give_get_to_service(info).text
    elements = json.loads(resp)['data']
    if not elements:
        print("Информация не найдена")
    for el in elements:
        link = 'https://egrp365.ru/reestr?egrp=' + el['cn']
        info_dict = get_space_and_floor_and_metres(link)
        insert_words_list(kadastr_num=el['cn'],
                          address=el['address'],
                          link_of_kadastr_num=link,
                          floor=info_dict['floor'],
                          json=json.dumps(el),
                          square=info_dict['metres'],
                          lat=info['lat'],
                          long=info['lon']
                          )
    # json.dumps(json_text, sort_keys=True, indent=4)
