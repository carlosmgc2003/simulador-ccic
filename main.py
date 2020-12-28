import logging

import model

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

if __name__ == '__main__':
    logging.info("Inició el programa")
    actor = model.PuestoComando()
    mensajes = []
    for _ in range(10):
        actor.generar_mm()
    for mensaje in actor.bandeja_salida:
        print(mensaje)
    logging.info("Finalizó el programa")

