
from logger.requests import metrics_insert


if __name__ == '__main__':
    for _ in range(1000):
        data = {'generador': 'Generador Redes Ext', 'tension': 0.0, 'corriente': 0.0}
        metrics_insert("alimentacion", data)