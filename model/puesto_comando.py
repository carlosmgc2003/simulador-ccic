from . import GeneradorMensajes
from .estafeta import Estafeta
from .facility import Facilidad


class PuestoComando(Facilidad):
    """PuestoComando genera los mensajes salientes del CCIC y recibe los mensajes entrantes."""

    def __init__(self, environment):
        super(PuestoComando, self).__init__(name="Puesto Comando", environment=environment)
        self.comandante = GeneradorMensajes()

    def generar_mm(self):
        nuevo_mm_saliente = self.comandante.generar_mensaje()
        nuevo_mm_saliente.destino = "Centro de Mensajes"
        self.bandeja_salida.append(nuevo_mm_saliente)
        print("mensaje generado")
        yield self.environment.timeout(5)

    def recibir_mm(self, estafeta: Estafeta):
        for mensaje in estafeta.bolsa_mensajes:
            if mensaje.destino == self.name:
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))
                print("Mensaje recibido del estafeta")

    def entregar_mm(self, estafeta: Estafeta):
        for mensaje in self.bandeja_salida:
            if mensaje.destino in list(map(lambda x: x.name, estafeta.recorrido)):
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))
                print("Mensaje entregado al estafeta")

    def operar(self):
        while True:
            yield self.environment.process(self.generar_mm())