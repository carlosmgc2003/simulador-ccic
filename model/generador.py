import random

from logger.requests import metrics_api
from model import TIEMPO_OCIOSO, DESV_STD_CONS_COMBUS, DESV_STD_TENSION, TENSION
from model.actor import Actor


class Generador(Actor):
    """ Generador representa a un grupo electrógeno con determinada capacidad, consumo y nivel inicial de combustible.
    El consumo varia en forma estándar por la constante DESV_STD_CONS_COMBUS.
    La tension TENSION varia de forma estándar con la DESV_STD_TENSION
    """

    def __init__(self, name, environment, capacidad_combus, consumo_combus, nivel_combus, db_connection):
        super(Generador, self).__init__(name=name, environment=environment, db_connection=db_connection)
        self.capacidad_combus = capacidad_combus
        self.consumo_combus = consumo_combus
        self.nivel_combus = nivel_combus
        self.encendido = False
        self.tension = 0.0

    def consumir_combustible(self):
        if self.nivel_combus > 0.0:
            disminucion = abs(random.normalvariate(self.consumo_combus, DESV_STD_CONS_COMBUS))
            self.nivel_combus -= disminucion
            self.encendido = True
            self.tension = random.normalvariate(TENSION, DESV_STD_TENSION)
        else:
            self.nivel_combus = 0.0
            self.encendido = False
            self.tension = 0.0

    def operar(self):
        while True:
            print(f'Turno de: {self.name}')
            self.consumir_combustible()
            self.reportar_nivel()
            self.reportar_tension()
            # nivel = self.medir_nivel()
            # tension = self.medir_tension()
            # self.writeApi.write(bucket="combustible-generador", org="ccic", record=nivel)
            # self.writeApi.write(bucket="tension-generador", org="ccic", record=tension)
            yield self.environment.timeout(TIEMPO_OCIOSO)

    def genera_electricidad(self):
        return self.encendido

    def reportar_nivel(self):
        data = {'generador': self.name, 'nivel': self.nivel_combus}
        metrics_api("nivel-combus", data)
        # return Point("litros") \
        #     .tag("identificacion", self.name) \
        #     .field("nivel", self.nivel_combus) \
        #     .time(datetime.utcnow(), WritePrecision.NS)

    def reportar_tension(self):
        data = {'generador': self.name, 'tension': self.tension}
        metrics_api("nivel-tension", data)
        # return Point("volts") \
        #     .tag("identificacion", self.name) \
        #     .field("tension", self.tension) \
        #     .time(datetime.utcnow(), WritePrecision.NS)
