
class Manager:
    def __init__(self, client):
        self.client = client

    def call(self, method, payload):
        return self.client.call(method, payload)
