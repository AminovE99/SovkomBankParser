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


if __name__ == '__main__':
    resp = give_post_to_service().text
    elements = json.loads(resp)['data']
    for el in elements:
        link = 'https://egrp365.ru/reestr?egrp='+el['cn']
        insert_words_list(kadastr_num=el['cn'],address=el['address'],link_of_kadastr_num=link,floor=None,json=json.dumps(el))
    # json.dumps(json_text, sort_keys=True, indent=4)
