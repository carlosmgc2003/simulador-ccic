import logging

import model

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.info("Inició el programa")
    actor = model.PuestoComando()
    mensajes = []
    for _ in range(10):
        actor.generar_mm_saliente()
    for mensaje in actor.bandeja_salida:
        print(mensaje)
    logging.info("Finalizó el programa")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
