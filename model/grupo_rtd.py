import random

from influxdb_client import WriteApi

from model import DESTINO_PROC_MM
from model.facility import Facilidad
from model.mensaje_militar import GeneradorMensajes


class GrupoRTD(Facilidad):
    """Cabina de radio transmision de datos que recibe los mensajes salientes del CCIC y los transmite y genera los mensajes entrantes."""

    def __init__(self, environment, red: str, db_connection: WriteApi):
        super(GrupoRTD, self).__init__(name="Red " + red, environment=environment, db_connection=db_connection)
        self.operador = GeneradorMensajes()

    def generar_mm(self):
        """ El GrupoRTD ingresa un mensaje al CCIC """
        nuevo_mm_saliente = self.operador.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        self.bandeja_salida.append(nuevo_mm_saliente)
        # Lugar para poner el tiempo aleatorio de generacion de mensajes
        yield self.environment.timeout(5)

    def transmitir_mm(self):
        """ Remover un mensaje de la bandeja de entrada y transmitirlo"""
        if self.bandeja_entrada:
            mensaje = self.bandeja_entrada.pop(0)
            print(f'{self.name}: TRANSMITIDO {mensaje}')
            # Lugar para poner el tiempo aleatorio de transmision de mensajes
            yield self.environment.timeout(random.randint(3, 6))
        else:
            yield self.environment.timeout(0)

    def operar(self):
        while True:
            yield self.environment.process(self.generar_mm())
            yield self.environment.process(self.transmitir_mm())
