
from random import random

from scipy.stats import norm

from model import DESTINO_PROC_MM, TIEMPO_OCIOSO, DEMANDA, TIEMPO_RECUPERACION
from model.facility import Facilidad
from model.generador import Generador
from model.mensaje_militar import GeneradorMensajes


class GrupoRTD(Facilidad):
    """Cabina de radio transmision de datos que recibe los mensajes salientes del CCIC y los transmite y genera los mensajes entrantes."""

    def __init__(self, environment, red: str, enchufado_a: Generador):
        super(GrupoRTD, self).__init__(name="Red " + red, environment=environment, enchufado_a=enchufado_a)
        self.operador = GeneradorMensajes()

    def generar_t_espera(self):
        return abs(norm.rvs() * TIEMPO_RECUPERACION)

    def generar_mm(self):
        """ El GrupoRTD ingresa un mensaje al CCIC """
        nuevo_mm_saliente = self.operador.generar_mensaje()
        nuevo_mm_saliente.destino = DESTINO_PROC_MM
        nuevo_mm_saliente.procedencia = self.name
        self.bandeja_salida.append(nuevo_mm_saliente)
        # Lugar para poner el tiempo aleatorio de generacion de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        # Registrar el dato para la BDSQL

    def transmitir_mm(self):
        """ Remover un mensaje de la bandeja de entrada y transmitirlo"""
        mensaje = self.bandeja_entrada.pop(0)
        print(f'{self.name}: TRANSMITIDO {mensaje}')
        # Lugar para poner el tiempo aleatorio de transmision de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        # Registrar el dato para la BDSQL

    def operar(self):
        while True:
            print(f'Turno de: {self.name}')
            probabilidad_trafico = random()
            self.reportar_long_cola()
            if self.generador.genera_electricidad():
                if not self.tiene_alimentacion:
                    self.poner_en_servicio()
                # Actividades del Gpo Rtef
                if probabilidad_trafico < DEMANDA:
                    yield self.environment.process(self.generar_mm())
                if len(self.bandeja_entrada) > 0:
                    yield self.environment.process(self.transmitir_mm())
            else:
                if self.tiene_alimentacion:
                    self.poner_fuera_servicio()
            self.tiene_alimentacion = self.generador.genera_electricidad()
            yield self.environment.timeout(TIEMPO_OCIOSO)
