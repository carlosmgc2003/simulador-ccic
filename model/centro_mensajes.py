import simpy
from scipy.stats import beta

from .estafeta import Estafeta
from .facility import Facilidad
from .mensaje_militar import MensajeMilitar


class CentroMensajes(Facilidad):
    """Clase que recibe coeficientes que modela los tiempos de servicio de procesamiento de mensajes.
    coeficientes : tuple = (p, q, a, b)"""

    def __init__(self, environment: simpy.Environment,coeficientes=(1.295, 1.902, 102.0, 720.0)):
        super(CentroMensajes, self).__init__(name="Centro de Mensajes", environment=environment)
        self.tiempo_ocioso = 0
        self.coeficientes = coeficientes
        self.fdp = beta(coeficientes[0], coeficientes[1])
        self.mensaje_en_proceso: MensajeMilitar = None

    def recibir_mm(self, estafeta: Estafeta):
        for mensaje in estafeta.bolsa_mensajes:
            if mensaje.destino == self.name:
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))
                # Agregar el registro de la hora de entrada al CM

    def entregar_mm(self, estafeta: Estafeta):
        for mensaje in self.bandeja_salida:
            if mensaje.destino in list(map(lambda x: x.name, estafeta.recorrido)):
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
                # Agregar el registro de la hora de salida del CM

    def generar_t_espera(self):
        return int(self.fdp.rvs() * (self.coeficientes[3] - self.coeficientes[2]) + self.coeficientes[2])

    def operar(self):
        while True:
            if self.bandeja_entrada:
                yield self.environment.process(self.procesar_mensaje())
            else:
                self.tiempo_ocioso += 1
                yield self.environment.timeout(1)

    def procesar_mensaje(self):
        """Generador de la acción del CM de procesar mensajes"""
        while True:
            tservicio = 2 # Aca debe ir el tiempo de servicio real
            self.mensaje_en_proceso: MensajeMilitar = self.bandeja_entrada.pop(0)
            # Agregar el registro del procesamiento en el mensaje
            yield self.environment.timeout(tservicio)
            # Escribir el nuevo destino en el mensaje (Por ahora todos al PC)
            self.mensaje_en_proceso.destino = "Puesto Comando"
            self.bandeja_salida.append(self.mensaje_en_proceso)
            yield self.environment.process(self.operar())
