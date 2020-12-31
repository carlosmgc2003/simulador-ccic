import random
from collections import namedtuple
from datetime import datetime

from influxdb_client import Point, WritePrecision

Metadata = namedtuple('Metadata', ['nro_mensaje', 'clasif_seg', 'precedencia', 'es_cifrado'])


class MensajeMilitar:
    """Clase que modela un mensaje militar. Las manos por las que pasa el mensaje se guarada en el atributo trace"""
    nro_inicial = 0

    def __init__(self, clasif_seg, precedencia, es_cifrado):
        self.metadata = Metadata(clasif_seg=clasif_seg, nro_mensaje=MensajeMilitar.nro_inicial + 1,
                                 precedencia=precedencia, es_cifrado=es_cifrado)
        self.trace = []
        self.destino = ""  # Proximo destino interno al que debe ir el MM
        self.procedencia = ""
        MensajeMilitar.nro_inicial += 1

    def __str__(self):
        """Representación cuando se hace print, legible para el humano."""
        return f'Nro MM: {self.metadata.nro_mensaje}, clasif_seg: ' \
               f'{self.metadata.clasif_seg}, ' \
               f'precedencia: {self.metadata.precedencia}, ' \
               f'destino: {self.destino}, ' \
               f'procedencia: {self.procedencia}'

    # TODO: que el mensaje guarde su trazabilidad en el atributo trace
    def to_point(self, facilidad: str, evento: str) -> Point:
        return Point("transaccion") \
            .tag("facilidad", facilidad) \
            .tag("destino", self.destino) \
            .tag("procedencia", self.procedencia) \
            .field(evento, self.metadata.nro_mensaje) \
            .time(datetime.utcnow(), WritePrecision.NS)


class GeneradorMensajes:
    """Clase que construye mensajes nuevos cuyos atributos son elegidos al azar. (Con distribucion de probabilidad
    constante"""
    precedencias = "rutina prioridad inmediato flash".split()
    clasificaciones = "público reservado confidencial secreto".split()

    def __init__(self):
        pass

    def generar_mensaje(self) -> MensajeMilitar:
        """Método que genera un mensaje cuyo contenido es aleatorio"""
        nueva_clasif_seg = self.generar_clasif_seg()
        nueva_precedencia = self.generar_precedencia()
        nuevo_cifrado = self.determinar_cifrado(nueva_clasif_seg)
        return MensajeMilitar(nueva_clasif_seg, nueva_precedencia, nuevo_cifrado)

    @staticmethod
    def generar_clasif_seg():
        """Elige al azar (equiprobable) alguna de las clasificaciones de seguridad"""
        return random.choice(GeneradorMensajes.clasificaciones)

    @staticmethod
    def generar_precedencia():
        """Elige al azar (equiprobable) alguna de las precedencias"""
        return random.choice(GeneradorMensajes.precedencias)

    @staticmethod
    def determinar_cifrado(clasif_seg):
        """Elige al azar (equiprobable) si el mensaje es cifrado o no entre aquellos cuya clasificacion de seguridad
        es acorde."""
        if clasif_seg in "confidencial secreto".split():
            return random.choice([True, False])
        else:
            return False
