from random import random

from scipy.stats import norm

from model import DESTINO_PROC_MM, DEMANDA, TIEMPO_OCIOSO, TIEMPO_RECUPERACION
from model.facility import Facilidad
from model.generador import Generador
from model.mensaje_militar import GeneradorMensajes


class PuestoComando(Facilidad):
    """PuestoComando genera los mensajes salientes del CCIC y recibe los mensajes entrantes."""

    def __init__(self, environment, enchufado_a: Generador):
        super(PuestoComando, self).__init__(name="Puesto Comando", environment=environment, enchufado_a=enchufado_a)
        self.comandante = GeneradorMensajes()

    def generar_t_espera(self):
        return abs(norm.rvs() * TIEMPO_RECUPERACION)

    def generar_mm(self):
        nuevo_mm_saliente = self.comandante.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        yield self.environment.timeout(self.generar_t_espera())
        self.bandeja_salida.append(nuevo_mm_saliente)
        self.reportar_evento_mm(mensaje=nuevo_mm_saliente, evento="generado")

    def operar(self):
        while True:
            print(f'Turno de: {self.name}')
            probabilidad_trafico = random()
            if probabilidad_trafico < DEMANDA:
                yield self.environment.process(self.generar_mm())
            yield self.environment.timeout(TIEMPO_OCIOSO)
