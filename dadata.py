import json

import requests

API_KEY = "dde0ba13e9b1d4527fe63a87c4094de61c40aa20"
BASE_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"


def get_useful_info(raw_address):
    headers = {"Authorization": "Token {}".format(API_KEY), "Content-Type": "application/json"}
    data = {"query": raw_address, "count": '1'}
    raw_address = requests.post(BASE_URL, data=json.dumps(data), headers=headers)
    suggest = raw_address.json()['suggestions'][0]['data']
    info = {"okato": suggest['okato'], "lat": suggest['geo_lat'], "lon": suggest['geo_lon'],
            "street_type": suggest["street_type_full"], "street": suggest["street"], "house_num": suggest['house'],
            'building_num': suggest['block'], "flat_num": suggest['flat']}
    return info
