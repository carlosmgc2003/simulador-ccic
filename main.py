import logging

import simpy

from logger.logger import influxdb_logger
from model.centro_mensajes import CentroMensajes
from model.estafeta import EstafetaConstante
from model.grupo_rtd import GrupoRTD
from model.puesto_comando import PuestoComando

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

if __name__ == '__main__':
    logging.info("Inició el programa")
    org = "ccic"
    bucket = "eventos-ccic"

    write_api = influxdb_logger()

    environment = simpy.Environment()
    pc = PuestoComando(environment, write_api)
    rtef1 = GrupoRTD(environment, "Cdo Op", write_api)
    rtef2 = GrupoRTD(environment, "Mat Pers", write_api)
    rtef3 = GrupoRTD(environment, "Icia", write_api)
    rtef4 = GrupoRTD(environment, "Cdo", write_api)
    rtef5 = GrupoRTD(environment, "Op", write_api)
    cm = CentroMensajes(environment, facilidades_ccic=[rtef1, rtef2, rtef3, rtef4, rtef5], db_connection=write_api)
    estafeta_pc = EstafetaConstante(environment, recorrido=[pc, cm], tiempo=30, db_connection=write_api)
    estafeta_local = EstafetaConstante(environment, recorrido=[rtef1, rtef2, rtef3, rtef4, rtef5, cm], tiempo=30,
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
    environment.run(until=3600)
    for mensaje in pc.bandeja_entrada:
        print(mensaje)
    write_api.close()
    logging.info("Finalizó el programa")
