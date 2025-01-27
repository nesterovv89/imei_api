import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


# Обращения к внешнему АПИ
def check_balance():
    url = 'https://api.imeicheck.net/v1/account'
    token = os.getenv('API_TOKEN')
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()


def check_services(imei=None):
    url_2 = 'https://api.imeicheck.net/v1/services'
    token = os.getenv('API_TOKEN')
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json',
    }
    body = json.dumps({
      'deviceId': str(imei),
    })
    response = requests.get(url_2, headers=headers, data=body)
    return response.json()


def get_service(imei, id):
    url_3 = 'https://api.imeicheck.net/v1/checks'
    token = token = os.getenv('API_TOKEN')
    headers = {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'application/json',
    }
    body = json.dumps({
      'deviceId': str(imei),
      'serviceId': id
    })
    response = requests.post(url_3, headers=headers, data=body)
    return response.json()
