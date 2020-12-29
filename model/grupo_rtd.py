from model import DESTINO_PROC_MM
from model.facility import Facilidad
from model.mensaje_militar import GeneradorMensajes


class GrupoRTD(Facilidad):
    """Cabina de radio transmision de datos que recibe los mensajes salientes del CCIC y genera los mensajes entrantes."""

    def __init__(self, environment, red: str):
        super(GrupoRTD, self).__init__(name="Red " + red, environment=environment)
        self.operador = GeneradorMensajes()

    def generar_mm(self):
        nuevo_mm_saliente = self.operador.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        self.bandeja_salida.append(nuevo_mm_saliente)
        yield self.environment.timeout(5)

    def operar(self):
        while True:
            yield self.environment.process(self.generar_mm())
