import logging

import simpy

from logger.logger import influxdb_logger
from model import TIEMPO_OCIOSO
from model.centro_mensajes import CentroMensajes
from model.estafeta import EstafetaConstante
from model.generador import Generador
from model.grupo_rtd import GrupoRTD
from model.puesto_comando import PuestoComando

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# Características Genenerador Electrogeno
# Grupo electrogeno Kawasaki
CAPACIDAD = 12.0  # Litros
CONSUMO_COMBUS = (
                         1.0 / 3600) * TIEMPO_OCIOSO  # 1 litro sobre 3600 segundos (hora) por TIEMPO_OCIOSO (menor unidad de resolucion de tiempo)
NIVEL_COMBUSTIBLE = 6.0

if __name__ == '__main__':
    logging.info("Inició el programa")
    try:
        write_api = influxdb_logger()
    except Exception as e:
        print(e)
        exit(1)
    t_recorrido_estaf = 30

    environment = simpy.Environment()
    generador1 = Generador(environment=environment, name="Generador CMD", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=NIVEL_COMBUSTIBLE, db_connection=write_api)
    generador2 = Generador(environment=environment, name="Generador Redes Ext", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=2, db_connection=write_api)
    generador3 = Generador(environment=environment, name="Generador Redes Int", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=NIVEL_COMBUSTIBLE, db_connection=write_api)
    generador4 = Generador(environment=environment, name="Generador PC", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=NIVEL_COMBUSTIBLE, db_connection=write_api)

    pc = PuestoComando(environment=environment, db_connection=write_api, enchufado_a=generador4)

    rtef1 = GrupoRTD(environment, "Cdo Op", db_connection=write_api, enchufado_a=generador3)
    rtef2 = GrupoRTD(environment, "Mat Pers", db_connection=write_api, enchufado_a=generador3)
    rtef3 = GrupoRTD(environment, "Icia", db_connection=write_api, enchufado_a=generador3)
    rtef4 = GrupoRTD(environment, "Cdo", db_connection=write_api, enchufado_a=generador2)
    rtef5 = GrupoRTD(environment, "Op", db_connection=write_api, enchufado_a=generador2)
    cm = CentroMensajes(environment, facilidades_ccic=[rtef1, rtef2, rtef3, rtef4, rtef5], db_connection=write_api,
                        enchufado_a=generador1)

    estafeta_pc = EstafetaConstante(environment, recorrido=[pc, cm], tiempo=t_recorrido_estaf, db_connection=write_api)
    estafeta_local = EstafetaConstante(environment, recorrido=[rtef1, rtef2, rtef3, rtef4, rtef5, cm],
                                       tiempo=t_recorrido_estaf,
                                       db_connection=write_api)

    environment.process(pc.operar())
    environment.process(estafeta_pc.operar())
    environment.process(estafeta_local.operar())
    environment.process(cm.operar())
    environment.process(rtef1.operar())
    environment.process(rtef2.operar())
    environment.process(rtef3.operar())
    environment.process(rtef4.operar())
    environment.process(rtef5.operar())
    environment.process(generador1.operar())
    environment.process(generador2.operar())
    environment.process(generador3.operar())
    environment.process(generador4.operar())
    environment.run(until=3600)
    write_api.close()
    logging.info("Finalizó el programa")
