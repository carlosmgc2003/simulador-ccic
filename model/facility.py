from typing import List

import simpy

from .actor import Actor
from .mensaje_militar import MensajeMilitar


class Facilidad(Actor):
    """Facilidad es una clase abstracta que reune las abstracciones en comun de las facilidades del CCIC, relacionadas
    con comunicaciones y logistica, asi como las conexiones con simpy"""

    def __init__(self, name, environment):
        super(Facilidad, self).__init__(name=name, environment=environment)
        self.bandeja_entrada: List[MensajeMilitar] = []
        self.bandeja_salida: List[MensajeMilitar] = []
        self.escribiente: simpy.Resource = simpy.Resource(environment, 1)

    def recibir_mm(self, estafeta):
        bolsa_mensajes = estafeta.bolsa_mensajes.copy()
        for mensaje in bolsa_mensajes:
            if mensaje.destino == self.name:
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))
                print(f'{self.name} RECIBIDO: {mensaje}')

    def entregar_mm(self, estafeta):
        bandeja_salida = self.bandeja_salida.copy()
        for mensaje in bandeja_salida:
            if mensaje.destino in list(map(lambda x: x.name, estafeta.recorrido)):
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
                print(f'{self.name} ENTREGADO: {mensaje}')
