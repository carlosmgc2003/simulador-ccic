import logging
import argparse


import simpy

from logger.requests import events_clear
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

parser = argparse.ArgumentParser()
parser.add_argument("tiempo", type=int,help="cantidad en segundos que dura la corrida de simulacion de ccic (tiempo > 0)")
parser.add_argument("--factor",type=float, default=1, help="factor de duracion de un tick de simulacion. Default: 1 (factor > 0.0)")
args = parser.parse_args()
if args.tiempo <= 0:
    logging.error("No puede ser negativo ni cero el tiempo de simulacion")
    exit(-1)
if args.factor <= 0.0:
    logging.error("No puede ser negativo ni cero el factor de tick de simulacion")
    exit(-1)

if __name__ == '__main__':
    logging.info("Inició el programa")
    events_clear("mens-mil")
    t_recorrido_estaf = 30

    environment = simpy.RealtimeEnvironment(factor=args.factor, strict=False)
    generador1 = Generador(environment=environment, name="Generador CMD", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=1)
    generador2 = Generador(environment=environment, name="Generador Redes Ext", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=2)
    generador3 = Generador(environment=environment, name="Generador Redes Int", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=3)
    generador4 = Generador(environment=environment, name="Generador PC", capacidad_combus=CAPACIDAD,
                           consumo_combus=CONSUMO_COMBUS, nivel_combus=4)

    pc = PuestoComando(environment=environment, enchufado_a=generador4)

    rtef1 = GrupoRTD(environment, "Cdo Op", enchufado_a=generador3)
    rtef2 = GrupoRTD(environment, "Mat Pers", enchufado_a=generador3)
    rtef3 = GrupoRTD(environment, "Icia", enchufado_a=generador3)
    rtef4 = GrupoRTD(environment, "Cdo", enchufado_a=generador2)
    rtef5 = GrupoRTD(environment, "Op", enchufado_a=generador2)
    cm = CentroMensajes(environment, facilidades_ccic=[rtef1, rtef2, rtef3, rtef4, rtef5], enchufado_a=generador1)

    estafeta_pc = EstafetaConstante(environment, recorrido=[pc, cm], tiempo=t_recorrido_estaf)
    estafeta_local = EstafetaConstante(environment, recorrido=[rtef1, rtef2, rtef3, rtef4, rtef5, cm],
                                       tiempo=t_recorrido_estaf // 5)

    environment.process(pc.operar())
    environment.process(estafeta_pc.operar())
    environment.process(estafeta_local.operar())
    environment.process(cm.operar())
    environment.process(rtef1.operar())
    environment.process(rtef2.operar())
    environment.process(rtef3.operar())
    environment.process(rtef4.operar())
    environment.process(rtef5.operar())
    environment.process(cm.monitoreo_horus())
    environment.process(rtef1.monitoreo_horus())
    environment.process(rtef2.monitoreo_horus())
    environment.process(rtef3.monitoreo_horus())
    environment.process(rtef4.monitoreo_horus())
    environment.process(rtef5.monitoreo_horus())
    environment.process(generador1.operar())
    environment.process(generador2.operar())
    environment.process(generador3.operar())
    environment.process(generador4.operar())
    environment.run(until=args.tiempo)
    events_clear("mens-mil")
    logging.info("Finalizó el programa")
