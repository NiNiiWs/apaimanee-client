import json
from .client import ApaimaneeClient

class ApaimaneeClientTest:
    def __init__(self):
        self.client = ApaimaneeClient()

    def login(self):

        response = self.client.user.login('Aran', '12345')
        print('login response: ', response)

    def register(self):

        response = self.client.user.register('Niniw', '12345', 'aran@hotmail.com', 'aran', 'khunaree')
        print('register response: ', response)

    def create(self):
        print('login first')


    def status(self):
        print('controller status')

    def start(self):
        self.client.initial()
        commands = dict(
                login = self.login,
                register = self.register,
                create = self.create,
                start = self.status
                )
        while True:
            print('Please Mode command:1.login 2.register 3.create 4.start')
            cmd = input('Enter command :')

            func = commands.get(cmd, None)
            if func is not None:
                func()

