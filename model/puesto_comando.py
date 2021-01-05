from influxdb_client import WriteApi
from scipy.stats import norm

from model import DESTINO_PROC_MM
from model.facility import Facilidad
from model.mensaje_militar import GeneradorMensajes


class PuestoComando(Facilidad):
    """PuestoComando genera los mensajes salientes del CCIC y recibe los mensajes entrantes."""

    def __init__(self, environment, db_connection: WriteApi):
        super(PuestoComando, self).__init__(name="Puesto Comando", environment=environment, db_connection=db_connection)
        self.comandante = GeneradorMensajes()

    def generar_t_espera(self):
        return abs(norm.rvs() * 300)

    def generar_mm(self):
        nuevo_mm_saliente = self.comandante.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        self.bandeja_salida.append(nuevo_mm_saliente)
        yield self.environment.timeout(self.generar_t_espera())

    def operar(self):
        while True:
            yield self.environment.process(self.generar_mm())