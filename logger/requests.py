import configparser
import json
import time

import requests

config = configparser.ConfigParser()
config.read("config.ini")
metrics_url = config['api-horus']['url_metricas']
events_url = config['api-horus']['url_eventos']


def metrics_api(endpoint: str, data: dict):
    data['timestamp'] = int(time.time())
    try:
        r = requests.post(metrics_url + endpoint, data=json.dumps(data, skipkeys=True), timeout=0.1)
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
    except requests.exceptions.ConnectionError:
        print("Problema con la conexion... Abortando...")
        exit(1)


def events_api(endpoint: str, data: dict):
    global r
    data['timestamp'] = int(time.time())
    try:
        r = requests.post(events_url + endpoint, data=json.dumps(data, skipkeys=True), timeout=0.1)
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
    except requests.exceptions.ConnectionError:
        print("Problema con la conexion... Abortando...")
        exit(1)
