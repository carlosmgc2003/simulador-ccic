import random
from typing import List

import simpy
from scipy.stats import beta

from model import PUESTO_COMANDO, TIEMPO_OCIOSO
from model.facility import Facilidad
from model.generador import Generador
from model.mensaje_militar import MensajeMilitar


class CentroMensajes(Facilidad):
    """Clase que recibe coeficientes que modela los tiempos de servicio de procesamiento de mensajes.
    coeficientes : tuple = (p, q, a, b)"""

    def __init__(self, environment: simpy.Environment, enchufado_a: Generador,
                 facilidades_ccic=None,
                 coeficientes=(1.295, 1.902, 102.0, 720.0)):
        super(CentroMensajes, self).__init__(name="Centro de Mensajes", environment=environment,
                                             enchufado_a=enchufado_a)
        if facilidades_ccic is None:
            facilidades_ccic = []
        self.tiempo_ocioso = 0
        self.coeficientes = coeficientes
        self.fdp = beta(coeficientes[0], coeficientes[1])
        self.facilidades_ccic: List[Facilidad] = facilidades_ccic


    def generar_t_espera(self):
        return int(self.fdp.rvs() * (self.coeficientes[3] - self.coeficientes[2]) + self.coeficientes[2])

    def operar(self):
        while True:
            print(f'Turno de: {self.name}')
            self.reportar_long_cola()
            self.reportar_estado_servicio()
            if self.generador.genera_electricidad():
                if not self.tiene_alimentacion:
                    self.poner_en_servicio()
                # Actividades del Gpo Rtef
                if len(self.bandeja_entrada) > 0:
                    yield self.environment.process(self.procesar_mensaje())
            else:
                if self.tiene_alimentacion:
                    self.poner_fuera_servicio()
                if len(self.bandeja_entrada) > 0:
                    yield self.environment.process(self.procesar_mensaje(penalizacion=1.5))
            self.tiene_alimentacion = self.generador.genera_electricidad()
            self.tiempo_ocioso += 5
            yield self.environment.timeout(TIEMPO_OCIOSO)

    def procesar_mensaje(self, penalizacion: float = 1.0):
        """Generador de la acción del CM de procesar mensajes"""
        tservicio = self.generar_t_espera() * penalizacion  # Aca debe ir el tiempo de servicio real
        mensaje_en_proceso: MensajeMilitar = self.bandeja_entrada.pop(0)
        # Agregar el registro del procesamiento en el mensaje
        yield self.environment.timeout(tservicio)
        # Escribir el nuevo destino en el mensaje (Por ahora todos al PC)
        self.encaminar_mensaje(mensaje_en_proceso)
        mensaje_en_proceso.procedencia = self.name
        self.bandeja_salida.append(mensaje_en_proceso)
        yield self.environment.process(self.operar())

    def encaminar_mensaje(self, mensaje: MensajeMilitar):
        nombres_facilidades = list(map(lambda x: x.name, self.facilidades_ccic))
        if mensaje.procedencia == PUESTO_COMANDO and len(nombres_facilidades) > 0:
            mensaje.destino = random.choice(nombres_facilidades)
        else:
            mensaje.destino = PUESTO_COMANDO
