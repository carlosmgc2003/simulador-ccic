from typing import List

import simpy
from influxdb_client import WriteApi

from .actor import Actor
from .generador import Generador
from .mensaje_militar import MensajeMilitar


class Facilidad(Actor):
    """Facilidad es una clase abstracta que reune las abstracciones en comun de las facilidades del CCIC, relacionadas
    con comunicaciones y logistica, asi como las conexiones con simpy"""

    def __init__(self, name: str, environment: simpy.Environment, db_connection: WriteApi, enchufado_a: Generador):
        super(Facilidad, self).__init__(name=name, environment=environment, db_connection=db_connection)
        self.bandeja_entrada: List[MensajeMilitar] = []
        self.bandeja_salida: List[MensajeMilitar] = []
        self.escribiente: simpy.Resource = simpy.Resource(environment, 1)
        self.generador = enchufado_a

    def recibir_mm(self, estafeta):
        bolsa_mensajes: List[MensajeMilitar] = estafeta.bolsa_mensajes.copy()
        for mensaje in bolsa_mensajes:
            if mensaje.destino == self.name:
                self.writeApi.write(bucket="mensajes-ccic", org="ccic", record=mensaje.to_point(self.name, "recibir"))
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))
                print(f'{self.name} RECIBIDO: {mensaje}')

    def entregar_mm(self, estafeta):
        bandeja_salida = self.bandeja_salida.copy()
        for mensaje in bandeja_salida:
            if mensaje.destino in list(map(lambda x: x.name, estafeta.recorrido)):
                self.writeApi.write(bucket="mensajes-ccic", org="ccic", record=mensaje.to_point(self.name, "entregar"))
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
                print(f'{self.name} ENTREGADO: {mensaje}')
