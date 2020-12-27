from . import GeneradorMensajes
from .estafeta import Estafeta
from .facility import Facilidad


class PuestoComando(Facilidad):
    """PuestoComando genera los mensajes salientes del CCIC y recibe los mensajes entrantes."""

    def __init__(self):
        super(PuestoComando, self).__init__(name="Puesto Comando")
        self.comandante = GeneradorMensajes()

    def generar_mm(self):
        nuevo_mm_saliente = self.comandante.generar_mensaje()
        nuevo_mm_saliente.destino = "Centro de Mensajes"
        self.bandeja_salida.append(nuevo_mm_saliente)

    def recibir_mm(self, estafeta: Estafeta):
        for mensaje in estafeta.bolsa_mensajes:
            if mensaje.destino == self.name:
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))

    def entregar_mm(self, estafeta: Estafeta):
        for mensaje in self.bandeja_salida:
            if mensaje.destino in estafeta.recorrido:
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
