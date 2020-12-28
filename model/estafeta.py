import simpy
from scipy.stats import norm

from model import *


class Estafeta(Actor):
    """Clase que modela el comportamiento del estafeta del centro de mensajes. Como los promotores están fuera de
    estudio, el llena su bolsa con mensajes"""

    def __init__(self, ambiente: simpy.Environment, tipo_estafeta: str, recorrido: list):
        super(Estafeta, self).__init__(name="Estafeta")
        self.bolsa_mensajes: List[MensajeMilitar] = []
        self.recorrido: List[Facilidad] = recorrido
        self.ambiente: simpy.Environment = ambiente
        self.tipo_estafeta: str = tipo_estafeta

    def recoger_mensaje(self, mensaje: MensajeMilitar) -> MensajeMilitar:
        self.bolsa_mensajes.append(mensaje)
        return mensaje

    def entregar_mensaje(self, mensaje: MensajeMilitar) -> MensajeMilitar:
        self.bolsa_mensajes.remove(mensaje)
        return mensaje

    def generar_t_recorrido(self) -> int:
        pass


class EstafetaNormal(Estafeta):
    """Estafeta cuyo tiempo de recorrido sigue una distribucion de probabilidad normal. Los valores por defecto se corres
    ponden a lo estudiado en Análisis del CM"""

    def __init__(self, ambiente: simpy.Environment, recorrido: list, media_recorrido=447.0714285714285,
                 desvest_recorrido=16.524583984151636):
        super().__init__(ambiente, tipo_estafeta='normal', recorrido=recorrido)
        self.media_recorrido = media_recorrido
        self.desvest_recorrido = desvest_recorrido
        pass

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return int(norm.rvs() * self.desvest_recorrido + self.media_recorrido)


class EstafetaUniforme(Estafeta):
    """Estafeta cuyo tiempo de recorrido es uan cantidad en segundos elegida entre 0 y maxtiempo de manera uniforme"""

    def __init__(self, ambiente: simpy.Environment, recorrido: list, maxtiempo: int):
        super().__init__(ambiente, tipo_estafeta='uniforme', recorrido=recorrido)
        self.maxtiempo = maxtiempo

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return random.randint(0, self.maxtiempo)


class EstafetaConstante(Estafeta):
    """Estafeta cuyo tiempo de recorrido es constante. Siempre tiene el mismo tiempo de recorrido. Por defecto 1000 seg"""

    def __init__(self, ambiente: simpy.Environment, recorrido: list, tiempo: int = 1000):
        super().__init__(ambiente, tipo_estafeta='constante', recorrido=recorrido)
        self.tiempo = tiempo

    def generar_t_recorrido(self):
        """Genera su tiempo de recorrido"""
        return self.tiempo
