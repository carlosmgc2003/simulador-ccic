from datetime import datetime

from influxdb_client import WriteApi, WritePrecision, Point
from scipy.stats import norm

from model import DESTINO_PROC_MM, TIEMPO_OCIOSO
from model.facility import Facilidad
from model.mensaje_militar import GeneradorMensajes


class GrupoRTD(Facilidad):
    """Cabina de radio transmision de datos que recibe los mensajes salientes del CCIC y los transmite y genera los mensajes entrantes."""

    def __init__(self, environment, red: str, db_connection: WriteApi):
        super(GrupoRTD, self).__init__(name="Red " + red, environment=environment, db_connection=db_connection)
        self.operador = GeneradorMensajes()

    def generar_t_espera(self):
        return abs(norm.rvs() * 150)

    def generar_mm(self):
        """ El GrupoRTD ingresa un mensaje al CCIC """
        nuevo_mm_saliente = self.operador.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        self.bandeja_salida.append(nuevo_mm_saliente)
        # Lugar para poner el tiempo aleatorio de generacion de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        self.registrar_mm("recibido", int(nuevo_mm_saliente.metadata.nro_mensaje))

    def transmitir_mm(self):
        """ Remover un mensaje de la bandeja de entrada y transmitirlo"""
        mensaje = self.bandeja_entrada.pop(0)
        print(f'{self.name}: TRANSMITIDO {mensaje}')
        # Lugar para poner el tiempo aleatorio de transmision de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        self.registrar_mm("transmitido", int(mensaje.metadata.nro_mensaje))

    def operar(self):
        while True:
            print(f"{self.name} Bandeja Salida:{len(self.bandeja_salida)} Bandeja Entrada: {len(self.bandeja_entrada)}")
            if len(self.bandeja_salida) == 0:
                yield self.environment.process(self.generar_mm())
            if len(self.bandeja_entrada) > 0:
                yield self.environment.process(self.transmitir_mm())
            yield self.environment.timeout(TIEMPO_OCIOSO)

    def registrar_mm(self, actividad, nro_mm):
        point = Point("mm") \
            .tag("facilidad", self.name) \
            .field(actividad, nro_mm) \
            .time(datetime.utcnow(), WritePrecision.NS)
        self.writeApi.write("gpos-rtef", "ccic", point)
