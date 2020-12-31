from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi

from logger import INFLUX_DB_TOKEN, INFLUX_DB_URL


def influxdb_logger() -> WriteApi:
    token = INFLUX_DB_TOKEN
    client = InfluxDBClient(url=INFLUX_DB_URL, token=token)
    return client.write_api(write_options=SYNCHRONOUS)
