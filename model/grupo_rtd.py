
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
        return int(abs(norm.rvs() * TIEMPO_RECUPERACION + TIEMPO_RECUPERACION))

    def generar_mm(self):
        """ El GrupoRTD ingresa un mensaje al CCIC """
        nuevo_mm_entrante = self.operador.generar_mensaje()
        nuevo_mm_entrante.destino = DESTINO_PROC_MM
        nuevo_mm_entrante.procedencia = self.name
        # Lugar para poner el tiempo aleatorio de generacion de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        self.bandeja_salida.append(nuevo_mm_entrante)
        self.reportar_evento_mm(mensaje=nuevo_mm_entrante, evento="recibido")
        # Registrar el dato para la BDSQL

    def transmitir_mm(self):
        """ Remover un mensaje de la bandeja de entrada y transmitirlo"""
        # Lugar para poner el tiempo aleatorio de transmision de mensajes
        yield self.environment.timeout(self.generar_t_espera())
        mensaje = self.bandeja_entrada.pop(0)
        print(f'{self.name}: TRANSMITIDO {mensaje}')
        self.reportar_evento_mm(mensaje=mensaje, evento="transmitido")
        # Registrar el dato para la BDSQL


    def monitoreo_horus(self):
        while True:
            self.reportar_long_cola(len(self.bandeja_salida))
            self.reportar_estado_servicio()
            self.reportar_sensores_bool()
            yield self.environment.timeout(TIEMPO_OCIOSO)

    def operar(self):
        while True:
            electricidad = self.generador.genera_electricidad()
            print(f'Turno de: {self.name} {self.estado}')
            probabilidad_trafico = random()
            if electricidad:
                if not self.tiene_alimentacion:
                    #print("ME PUSE EN SERVICIO")
                    self.poner_en_servicio()
                # Actividades del Gpo Rtef
                if probabilidad_trafico < DEMANDA:
                    yield self.environment.process(self.generar_mm())
                if len(self.bandeja_entrada) > 0:
                    yield self.environment.process(self.transmitir_mm())
            else:
                if self.tiene_alimentacion:
                    #print("ME PUSE FUERA DE SERVICIO")
                    self.poner_fuera_servicio()
            self.tiene_alimentacion = electricidad
            yield self.environment.timeout(TIEMPO_OCIOSO)


