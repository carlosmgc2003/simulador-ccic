import logging

import model

import simpy

from model.centro_mensajes import CentroMensajes
from model.estafeta import EstafetaUniforme
from model.puesto_comando import PuestoComando

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

if __name__ == '__main__':
    logging.info("Inició el programa")
    environment = simpy.Environment()
    cm = CentroMensajes(environment)
    pc = PuestoComando(environment)
    estafeta = EstafetaUniforme(environment, recorrido=[cm, pc], maxtiempo=3)
    environment.process(pc.operar())
    environment.process(estafeta.operar())
    environment.process(cm.operar())
    environment.run(until=20)
    for mensaje in pc.bandeja_entrada:
        print(mensaje)
    logging.info("Finalizó el programa")

