import configparser
import json
import time

import requests
import urllib3

config = configparser.ConfigParser()
config.read("config.ini")
metrics_url = config['api-horus']['url_metricas']
events_url = config['api-horus']['url_eventos']
token_url = config['api-horus']['url_token']
grafana_user = config['api-horus']['grafana_user']
grafana_pass = config['api-horus']['grafana_pass']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bearer_token():
    try:
        r = requests.get(f'{token_url}list?user={grafana_user}&pass={grafana_pass}', timeout=10, verify=False)
        if r.status_code == 200:
            json_response = r.json()
            try:
                token_simulador = json_response["simulador"]
                if len(token_simulador) == 32:
                    return token_simulador
            except KeyError:
                r = requests.get(f'{token_url}generate?user={grafana_user}&pass={grafana_pass}&device=simulador', timeout=10, verify=False)
                if r.status_code == 200:
                    json_response = r.json()
                    return json_response["token"]
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
        exit(1)
    except requests.exceptions.ConnectionError as e:
        print("Problema con la conexion... Abortando...")
        exit(1)


bearer_token = get_bearer_token()

headers = {"Authorization": "Bearer " + bearer_token}


def api_post(url: str, endpoint: str, body: str):
    try:
        r = requests.post(url + endpoint, data=body, timeout=10, headers=headers, verify=False)
    except requests.exceptions.Timeout:
        print("Se agoto el tiempo de espera...")
    except requests.exceptions.ConnectionError as e:
        print("Problema con la conexion... Abortando...")
        print(e)
        exit(1)


def api_delete(url: str, endpoint: str):
    try:
        r = requests.delete(url + endpoint, timeout=10, headers=headers, verify=False)
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
