from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi


def influxdb_logger() -> WriteApi:
    """ Funcion que retorna una instancia de WriteApi, de acuerdo a los parametros de conexion a la BD """
    client = InfluxDBClient.from_config_file("config.ini")
    bucket_api = client.buckets_api()
    return client.write_api(write_options=SYNCHRONOUS)
