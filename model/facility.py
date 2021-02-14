from typing import List

import simpy

from logger.requests import metrics_insert, events_insert
from .actor import Actor
from .generador import Generador
from .mensaje_militar import MensajeMilitar

ESTADOS = ["en servicio", "servicio limitado", "fuera servicio"]

class Facilidad(Actor):
    """Facilidad es una clase abstracta que reune las abstracciones en comun de las facilidades del CCIC, relacionadas
    con comunicaciones y logistica, asi como las conexiones con simpy"""

    def __init__(self, name: str, environment: simpy.Environment, enchufado_a: Generador):
        super(Facilidad, self).__init__(name=name, environment=environment)
        self.bandeja_entrada: List[MensajeMilitar] = []
        self.bandeja_salida: List[MensajeMilitar] = []
        self.escribiente: simpy.Resource = simpy.Resource(environment, 1)
        self.generador = enchufado_a
        self.estado = ESTADOS[2]
        self.tiene_alimentacion = False

    def recibir_mm(self, estafeta):
        bolsa_mensajes: List[MensajeMilitar] = estafeta.bolsa_mensajes.copy()
        for mensaje in bolsa_mensajes:
            if mensaje.destino == self.name:
                self.reportar_evento_mm(mensaje=mensaje, evento="recibir")
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))
                print(f'{self.name} RECIBIDO: {mensaje}')

    def entregar_mm(self, estafeta):
        bandeja_salida = self.bandeja_salida.copy()
        for mensaje in bandeja_salida:
            if mensaje.destino in list(map(lambda x: x.name, estafeta.recorrido)):
                self.reportar_evento_mm(mensaje=mensaje, evento="entregar")
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
                print(f'{self.name} ENTREGADO: {mensaje}')

    def poner_en_servicio(self):
        self.estado = ESTADOS[0]
        self.reportar_estado_servicio()

    def poner_fuera_servicio(self):
        self.estado = ESTADOS[2]
        self.reportar_estado_servicio()

    def reportar_estado_servicio(self):
        data = {"facilidad": self.name, "estado": self.estado}
        metrics_insert("estado-servicio", data)

    def reportar_long_cola(self):
        data = {"facilidad": self.name, "long_cola": len(self.bandeja_entrada)}
        metrics_insert("longitud-cola", data)

    def reportar_evento_mm(self, mensaje: MensajeMilitar, evento: str):
        print("Mensaje")
        events_insert("mens-mil", mensaje.to_dict(evento))
