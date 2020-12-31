import random
from typing import List

import simpy
from influxdb_client import WriteApi
from scipy.stats import norm

from model.actor import Actor
from model.facility import Facilidad
from model.mensaje_militar import MensajeMilitar


class Estafeta(Actor):
    """Clase que modela el comportamiento del estafeta del centro de mensajes. Como los promotores están fuera de
    estudio, el llena su bolsa con mensajes"""
    nro_estafeta = 1

    def __init__(self, environment: simpy.Environment, tipo_estafeta: str, recorrido: list, db_connection: WriteApi):
        super(Estafeta, self).__init__(name=f'Estafeta {Estafeta.nro_estafeta}', environment=environment,
                                       db_connection=db_connection)
        self.bolsa_mensajes: List[MensajeMilitar] = []
        self.recorrido: List[Facilidad] = recorrido
        self.environment: simpy.Environment = environment
        self.tipo_estafeta: str = tipo_estafeta
        Estafeta.nro_estafeta += 1

    def recoger_mensaje(self, mensaje: MensajeMilitar) -> MensajeMilitar:
        self.bolsa_mensajes.append(mensaje)
        return mensaje

    def entregar_mensaje(self, mensaje: MensajeMilitar) -> MensajeMilitar:
        self.bolsa_mensajes.remove(mensaje)
        return mensaje

    def generar_t_recorrido(self) -> int:
        pass

    def operar(self):
        while True:
            for facilidad in self.recorrido:
                with facilidad.escribiente.request() as req:
                    yield req
                    print(f'{self.name}: Visitando: {facilidad.name}')
                    facilidad.entregar_mm(self)
                    facilidad.recibir_mm(self)
                    yield self.environment.timeout(2)  # Tiempo que toma hablar con el escribiente
                    print(f'{self.name}: Bolsa:')
                    self.imprimir_bolsa()
                    yield self.environment.timeout(self.generar_t_recorrido())

    def imprimir_bolsa(self):
        for mensaje in self.bolsa_mensajes:
            print(mensaje)
        print('---------------------------')


class EstafetaNormal(Estafeta):
    """Estafeta cuyo tiempo de recorrido sigue una distribucion de probabilidad normal. Los valores por defecto se corres
    ponden a lo estudiado en Análisis del CM"""

    def __init__(self, ambiente: simpy.Environment, recorrido: list, db_connection: WriteApi,
                 media_recorrido=447.0714285714285,
                 desvest_recorrido=16.524583984151636):
        super().__init__(ambiente, tipo_estafeta='normal', recorrido=recorrido, db_connection=db_connection)
        self.media_recorrido = media_recorrido
        self.desvest_recorrido = desvest_recorrido
        pass

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return int(norm.rvs() * self.desvest_recorrido + self.media_recorrido)


class EstafetaUniforme(Estafeta):
    """Estafeta cuyo tiempo de recorrido es uan cantidad en segundos elegida entre 0 y maxtiempo de manera uniforme"""

    def __init__(self, ambiente: simpy.Environment, recorrido: list, maxtiempo: int, db_connection: WriteApi):
        super().__init__(ambiente, tipo_estafeta='uniforme', recorrido=recorrido, db_connection=db_connection)
        self.maxtiempo = maxtiempo

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return random.randint(0, self.maxtiempo)


class EstafetaConstante(Estafeta):
    """Estafeta cuyo tiempo de recorrido es constante. Siempre tiene el mismo tiempo de recorrido. Por defecto 1000 seg"""

    def __init__(self, environment: simpy.Environment, recorrido: list, db_connection: WriteApi, tiempo: int = 1000):
        super().__init__(environment, tipo_estafeta='constante', recorrido=recorrido, db_connection=db_connection)
        self.tiempo = tiempo

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return self.tiempo


class RedLan(Estafeta):
    """El estafeta instantáneo. Lleva los mensajes en un diferencial de tiempo"""

    def __init__(self, environment: simpy.Environment, recorrido: list, db_connection: WriteApi):
        super().__init__(environment=environment, tipo_estafeta='Red LAN', recorrido=recorrido,
                         db_connection=db_connection)
        self.tiempo = 0
