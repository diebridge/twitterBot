import requests
from bs4 import BeautifulSoup


PROXY_URL = 'https://free-proxy-list.net/'


def get_proxy():
    response = requests.get(PROXY_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('table',id='proxylisttable')
    list_tr = table.find_all('tr')
    list_td = [elem.find_all('td') for elem in list_tr]
    list_td = list(filter(None, list_td))
    list_ip = [elem[0].text for elem in list_td]
    list_ports = [elem[1].text for elem in list_td]
    list_proxies = [':'.join(elem) for elem in list(zip(list_ip, list_ports))]
    for proxy in list_proxies:
        yield proxy

# print(next(get_proxy()))
import json

def get_json(json_input):
    with open(json_input, 'r') as read_file:
        data = json.load(read_file)
        return data

print(len(get_json('tweets.json')))