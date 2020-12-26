from . import Actor
from . import GeneradorMensajes


class PuestoComando(Actor):
    """PuestoComando genera los mensajes salientes del CCIC y recibe los mensajes entrantes."""
    def __init__(self):
        super(PuestoComando, self).__init__(name="Puesto Comando")
        self.comandante = GeneradorMensajes()
        self.bandeja_entrada = []
        self.bandeja_salida = []

    def generar_mm_saliente(self):
        nuevo_mm_saliente = self.comandante.generar_mensaje()
        nuevo_mm_saliente.destino = "Centro de Mensajes"
        self.bandeja_salida.append(self.comandante.generar_mensaje())

    def recibir_mm_entrante(self, estafeta):
        # TODO: Hacer que "Deje" los mensajes entrantes
        pass
