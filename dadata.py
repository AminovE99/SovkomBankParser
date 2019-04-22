import json

import requests

API_KEY = "dde0ba13e9b1d4527fe63a87c4094de61c40aa20"
BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"


def get_useful_info_from_dadata(raw_address):
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    data = {"query": raw_address, "count": '1'}
    raw_address = requests.post(BASE_URL, data=json.dumps(data), headers=headers)
    try:
        suggest = raw_address.json()['suggestions'][0]['data']
    except IndexError:
        return {"postal_code": None,
            "lat": None,
            "lon": None,
            "street_type": None,
            "street": None,
            "house_num": None,
            'building_num': None,
            "flat_num": None,
            "region": None,
            "country": None,
            "city": None,
            "fias_id": None}
    building_num = None
    flat_num = None
    if suggest['block'] is not None:
        try:
            building_num = int(suggest['block'])
        except ValueError:
            print("ErrorMessage: Корпус дома записан неккоректно")
    if suggest['flat'] is not None:
        try:
            flat_num = int(suggest['flat'])
        except ValueError:
            print("ErrorMessage: Квартира записана неккоректно")
    info = {"postal_code": suggest['postal_code'],
            "lat": suggest['geo_lat'],
            "lon": suggest['geo_lon'],
            "street_type": suggest["street_type_full"],
            "street": suggest["street"],
            "house_num": suggest['house'],
            'building_num': building_num,
            "flat_num": flat_num,
            "region": suggest['region'],
            "country": suggest['country'],
            "city": suggest['city'],
            "fias_id": suggest['fias_id']}
    return info
