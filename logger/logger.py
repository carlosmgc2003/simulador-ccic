from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi


def influxdb_logger() -> WriteApi:
    """ Funcion que retorna una instancia de WriteApi, de acuerdo a los parametros de conexion a la BD """
    client = InfluxDBClient.from_config_file("config.ini")
    response = client.health()
    if response.status == 'fail':
        raise Exception("No se puede conectar a TSDB InfluxDB, compruebe la conexion de red")
    return client.write_api(write_options=SYNCHRONOUS)
