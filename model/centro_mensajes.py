from scipy.stats import beta

from model import Estafeta, Facilidad


class CentroMensajes(Facilidad):
    """Clase que recibe coeficientes que modela los tiempos de servicio de procesamiento de mensajes.
    coeficientes : tuple = (p, q, a, b)"""

    def __init__(self, coeficientes=(1.295, 1.902, 102.0, 720.0)):
        self.coeficientes = coeficientes
        self.fdp = beta(coeficientes[0], coeficientes[1])
        self.mensaje_en_proceso = None

    def recibir_mm(self, estafeta: Estafeta):
        for mensaje in estafeta.bolsa_mensajes:
            if mensaje.destino == self.name:
                self.bandeja_entrada.append(estafeta.entregar_mensaje(mensaje))

    def entregar_mm(self, estafeta: Estafeta):
        for mensaje in self.bandeja_salida:
            if mensaje.destino in estafeta.recorrido:
                self.bandeja_salida.remove(estafeta.recoger_mensaje(mensaje))

    def generar_t_espera(self):
        return int(self.fdp.rvs() * (self.coeficientes[3] - self.coeficientes[2]) + self.coeficientes[2])

    def revisar_mensajes(self):
        while True:
            if self.bandeja_entrada:
                yield self.ambiente.process(self.procesar_mensaje())
            else:
                self.tiempo_ocioso += 1
                yield self.ambiente.timeout(1)

    def procesar_mensaje(self):
        """Generador de la acción del CM de procesar mensajes"""
        while True:
            tservicio = self.generar_t_espera()
            tiempo_actual = self.ambiente.now
            self.mensaje_en_proceso = self.cola_mensajes.popleft()
            self.mensaje_en_proceso['datos']['tiempo_salida_cola'] = tiempo_actual
            # datetime.fromtimestamp(tiempo_actual + time()).strftime("%d/%m %I:%M:%S")
            # print(f'\x1b[1;34;40mCen Msj:\x1b[0m\t [{tiempo_actual}] {self.mensaje_en_proceso}
            # inició su procesamiento.')
            yield self.ambiente.timeout(tservicio)
            self.mensaje_en_proceso['datos']['tiempo_servicio'] = tservicio
            self.mensajes_procesados.append(self.mensaje_en_proceso)
            if self.stdout:
                print(
                    f'\x1b[1;34;40mCen Msj:\x1b[0m\t [{tiempo_actual}] {self.mensaje_en_proceso} finalizó su procesamiento.')
            yield self.ambiente.process(self.revisar_mensajes())

    def informar_cola(self):
        while True:
            yield self.ambiente.timeout(60)
            self.estados_cola.append({'tiempo': self.ambiente.now, 'long_cola': len(self.cola_mensajes)})
