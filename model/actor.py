import simpy


class Actor:
    """Clase abstracta que representa a todos los objetos de modelo que participan de la simulación"""

    def __init__(self, name: str, environment: simpy.Environment):
        self.environment = environment
        if len(name) > 0:
            self.name = name
        else:
            raise ValueError("No se puede utilizar la cadena nula")

    def __str__(self):
        return self.name
