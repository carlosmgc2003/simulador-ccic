import uuid


class Actor:
    def __init__(self, name: str):
        self.name = name
        self.uuid = uuid.uuid4()

    def __str__(self):
        return self.name + " " + str(self.uuid)
