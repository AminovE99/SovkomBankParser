import requests

address = "г Санкт-Петербург, ул Репищева, д 21 к 1"

url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
data = {"query": "г Санкт-Петербург, ул Репищева, д 21 к 1", "count": 1}
print(requests.post(url, data).text)