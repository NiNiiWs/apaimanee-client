import json
from .client import ApaimaneeClient

class ApaimaneeClientTest:
    def __init__(self):
        self.client = ApaimaneeClient()

    def login(self):

        response = self.client.user.login('username', 'password')
        print('login response: ', response)

    def create(self):
        print('login first')

    def status(self):
        print('controller status')

    def start(self):
        self.client.initial()
        commands = dict(
                l=self.login,
                c=self.create,
                s=self.status
                )
        while True:
            cmd = input('Enter command:')
            func = commands.get(cmd, None)
            if func is not None:
                func()

