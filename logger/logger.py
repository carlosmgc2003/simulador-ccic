from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi

from logger import INFLUX_DB_TOKEN, INFLUX_DB_URL


def influxdb_logger() -> WriteApi:
    """ Funcion que retorna una instancia de WriteApi, de acuerdo a los parametros de conexion a la BD """
    token = INFLUX_DB_TOKEN
    client = InfluxDBClient(url=INFLUX_DB_URL, token=token)
    return client.write_api(write_options=SYNCHRONOUS)
