from model import *


class Facilidad(Actor):
    """Facilidad es una clase abstracta que reune las abstracciones en comun de las facilidades del CCIC, relacionadas
    con comunicaciones y logistica, asi como las conexiones con simpy"""

    def __init__(self, name):
        super(Facilidad, self).__init__(name=name)
        self.bandeja_entrada: List[MensajeMilitar] = []
        self.bandeja_salida: List[MensajeMilitar] = []

    def recibir_mm(self, estafeta):
        pass

    def entregar_mm(self, estafeta):
        pass
