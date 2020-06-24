class ContainerPayload:
    def __init__(self, container):
        self.id = container.id
        self.name = container.name
        self.ports = container.ports
        self.labels = container.labels
        self.status = container.status

    def json(self):
        return self.__dict__