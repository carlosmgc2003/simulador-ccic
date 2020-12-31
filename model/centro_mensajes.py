import random
from datetime import datetime
from typing import List

import simpy
from influxdb_client import WriteApi, WritePrecision, Point
from scipy.stats import beta

from model import PUESTO_COMANDO
from model.facility import Facilidad
from model.mensaje_militar import MensajeMilitar


class CentroMensajes(Facilidad):
    """Clase que recibe coeficientes que modela los tiempos de servicio de procesamiento de mensajes.
    coeficientes : tuple = (p, q, a, b)"""

    def __init__(self, environment: simpy.Environment, db_connection: WriteApi, facilidades_ccic=None,
                 coeficientes=(1.295, 1.902, 102.0, 720.0)):
        super(CentroMensajes, self).__init__(name="Centro de Mensajes", environment=environment,
                                             db_connection=db_connection)
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
            self.registrar_long_cola()
            if self.bandeja_entrada:
                yield self.environment.process(self.procesar_mensaje())
            else:
                self.tiempo_ocioso += 1
                yield self.environment.timeout(1)

    def procesar_mensaje(self):
        """Generador de la acción del CM de procesar mensajes"""
        while True:
            tservicio = 2  # Aca debe ir el tiempo de servicio real
            mensaje_en_proceso: MensajeMilitar = self.bandeja_entrada.pop(0)
            print(f'PROCESO: {mensaje_en_proceso}')
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

    def registrar_long_cola(self):
        point = Point("long_cola") \
            .field("mm_en_espera", len(self.bandeja_entrada)) \
            .time(datetime.utcnow(), WritePrecision.NS)
        self.writeApi.write("cola_cmd", "ccic", point)
