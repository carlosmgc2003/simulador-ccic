import uuid


class Actor:
    def __init__(self, name: str):
        if len(name) > 0:
            self.name = name
        else:
            raise ValueError("No se puede utilizar la cadena nula")
        self.uuid = uuid.uuid4()

    def __str__(self):
        return self.name + " " + str(self.uuid)
