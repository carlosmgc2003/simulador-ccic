import configparser
import json
import time

import requests

config = configparser.ConfigParser()
config.read("config.ini")
metrics_url = config['api-horus']['url_metricas']
events_url = config['api-horus']['url_eventos']


def api_post(url: str, endpoint: str, body: str):
    try:
        r = requests.post(url + endpoint, data=body, timeout=0.1)
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
    except requests.exceptions.ConnectionError:
        print("Problema con la conexion... Abortando...")
        exit(1)


def api_delete(url: str, endpoint: str):
    try:
        r = requests.delete(url + endpoint, timeout=0.1)
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
    except requests.exceptions.ConnectionError:
        print("Problema con la conexion... Abortando...")
        exit(1)


def metrics_insert(endpoint: str, data: dict):
    data['timestamp'] = int(time.time())
    body = json.dumps(data, skipkeys=True)
    api_post(metrics_url, endpoint, body)


def events_insert(endpoint: str, data: dict):
    data['timestamp'] = int(time.time())
    body = json.dumps(data, skipkeys=True)
    api_post(events_url, endpoint, body)


def events_clear(endpoint: str):
    api_delete(events_url, endpoint)
