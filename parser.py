import json
import re

import requests
from bs4 import BeautifulSoup

from dadata import get_useful_info_from_dadata
from database import insert_words_list, insert_unfoundable_word


# Респ Коми, г Печора, Печорский пр-кт, д 116, кв 5
# ?street={info['street']}&house={info['house_num']}&building={info['building_num']}&mregion={info['region']}&area=null&city={info['city']}&apartment={info['flat_num']}&link=page&fiasid={info['fias_id']}


def not_found_info(handled_country,
                   handled_region,
                   handled_city,
                   handled_street,
                   handled_house_num,
                   handled_block,
                   handled_flat):
    insert_unfoundable_word(handled_country,handled_region,handled_city,handled_street,handled_house_num,handled_block,handled_flat)


def give_get_to_service(info):
    '''

    :param info: словарь в котором хранится вся информация об объекте
    :return: json
    '''
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


def get_raw_info_dict(link):
    soup = BeautifulSoup(''.join(requests.get(link).text), features="html.parser")
    info = soup.find('div', {"id": "information_about_object"}).contents
    info = str(info)
    floor = None
    founded_address_from_site = None
    try:
        # place = info.split('Описание —')[1].split("<br")  # кварти
        founded_address_from_site = info.split("Другое написание адреса — ")[1].split("<br")[
            0]  # убрав эту строчку, мы получим больше найденных адресов
    except IndexError:
        print('Не получилось найти handled_adress')

    try:
        floor = int(info.split('Этаж —')[1].split("<br")[0].split("эт")[0])  # этаж
    except IndexError:
        print('InfoMessage: Этажа нет')
    except ValueError:
        print("ErrorMessage: Этаж записан не числом")
    metres = float(info.split('Площадь —')[1].split("<br")[0].split('кв.м')[0])
    info_dict = {'floor': floor, 'metres': metres, 'handled_address': founded_address_from_site}
    print(f"info_dict: {info_dict}")
    return info_dict


def one_str_address(address):
    info = get_useful_info_from_dadata(address)
    resp = give_get_to_service(info).text
    element = json.loads(resp)
    if element['error'] == 1:
        print("Информация не найдена")
        not_found_info(handled_country=info['country'],
                       handled_region=info['region'],
                       handled_city=info['city'],
                       handled_street=info['street'],
                       handled_house_num=info['house_num'],
                       handled_block=info['building_num'],
                       handled_flat=info['flat_num']
                       )
        return -1
    egrp = element['data'].split('reestr?egrp=')[1].split('\'')[0]  # Хардкод! Поменять на регулярки
    link = 'https://egrp365.ru/reestr?egrp=' + egrp
    raw_info_dict = get_raw_info_dict(link)
    new_info_from_site = get_useful_info_from_dadata(raw_info_dict['handled_address'])
    insert_words_list(kadastr_num=egrp,
                      postal_code=info['postal_code'],
                      raw_country=new_info_from_site['country'],
                      raw_region=new_info_from_site['region'],
                      raw_city=new_info_from_site['city'],
                      raw_street=new_info_from_site['street'],
                      raw_house_num=new_info_from_site['house_num'],
                      raw_block=new_info_from_site['building_num'],
                      raw_flat=new_info_from_site['flat_num'],
                      handled_country=info['country'],
                      handled_region=info['region'],
                      handled_city=info['city'],
                      handled_street=info['street'],
                      handled_house_num=info['house_num'],
                      handled_block=info['building_num'],
                      handled_flat=info['flat_num'],
                      link_of_kadastr_num=link,
                      floor=raw_info_dict['floor'],
                      json=resp,
                      square=raw_info_dict['metres'],
                      latitude=info['lat'],
                      longitude=info['lon'])
    print("______________________________________________")


if __name__ == '__main__':
    print("1. Написать адрес одной строкой\n"
          "2. Расширенный поиск\n"
          "3. Считать все с файла data.txt (custom)")
    choice = input("Введите желаемое действие: ")
    address = None
    result = -1
    if choice == '1':
        address = input("Напишите адрес, где расположен дом: ")
    if choice == '2':  # Лучше не использовать else, потому что функционал может дополниться
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
    if choice == '3':
        file = open('data.txt', encoding='utf-8')
    for line in file:
        one_str_address(line)  # TODO: сделать запись данных в бд одной транзакцией
    count = 0
    while result == -1 and count <= 3:
        result = one_str_address(address)  # не используется boolean для возможности расширения функционала
        count += 1
