import logging

import simpy

from model.centro_mensajes import CentroMensajes
from model.estafeta import EstafetaUniforme
from model.grupo_rtd import GrupoRTD
from model.puesto_comando import PuestoComando

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

if __name__ == '__main__':
    logging.info("Inició el programa")
    environment = simpy.Environment()

    pc = PuestoComando(environment)
    rtef1 = GrupoRTD(environment, "Cdo Op")
    rtef2 = GrupoRTD(environment, "Mat Pers")
    rtef3 = GrupoRTD(environment, "Icia")
    rtef4 = GrupoRTD(environment, "Cdo")
    rtef5 = GrupoRTD(environment, "Op")
    cm = CentroMensajes(environment, facilidades_ccic=[rtef1, rtef2, rtef3, rtef4, rtef5])
    estafeta_pc = EstafetaUniforme(environment, recorrido=[pc, cm], maxtiempo=3)
    estafeta_local = EstafetaUniforme(environment, recorrido=[rtef1, rtef2, rtef3, rtef4, rtef5, cm], maxtiempo=3)
    environment.process(pc.operar())
    environment.process(estafeta_pc.operar())
    environment.process(estafeta_local.operar())
    environment.process(cm.operar())
    environment.process(rtef1.operar())
    environment.process(rtef2.operar())
    environment.process(rtef3.operar())
    environment.process(rtef4.operar())
    environment.process(rtef5.operar())
    environment.run(until=30)
    for mensaje in pc.bandeja_entrada:
        print(mensaje)
    logging.info("Finalizó el programa")
