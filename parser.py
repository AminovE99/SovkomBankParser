import json
import re

import requests
from bs4 import BeautifulSoup

from database import insert_words_list


def give_post_to_service():
    url = "https://extra.egrp365.ru/api/extra/index.php"
    data = {
        "macroRegionId": "192000000000",
        "regionId": "192401000000",
        "settlementId": "192401380000",
        "streetType": "str1",
        "street": "Глазунова",
        "method": "searchByAddress"
    }
    headers = {'user-agent': 'Mozilla/5.0'}
    return requests.post(url, data=data, headers=headers)


def get_space_and_floor_and_metres(link):
    soup = BeautifulSoup(''.join(requests.get(link).text))
    info = soup.find('div', {"id": "information_about_object"}).contents
    info = str(info)
    floor = None
    place = info.split('Описание —')[1].split("<br")[0]  # квартира
    try:
        floor = info.split('Этаж —')[1].split("<br")[0] # этаж
    except IndexError:
        print('этажа нет')
    metres = info.split('Площадь —')[1].split("<br")[0]
    info_dict = {'place': place, 'floor': floor, 'metres': metres}
    return info_dict


if __name__ == '__main__':
    resp = give_post_to_service().text
    elements = json.loads(resp)['data']
    for el in elements:
        link = 'https://egrp365.ru/reestr?egrp=' + el['cn']
        info_dict = get_space_and_floor_and_metres(link)
        insert_words_list(kadastr_num=el['cn'],
                          address=el['address'],
                          link_of_kadastr_num=link,
                          floor=info_dict['floor'],
                          json=json.dumps(el),
                          square=info_dict['metres']
                          )
    # json.dumps(json_text, sort_keys=True, indent=4)
