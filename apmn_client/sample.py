import json
from .client import ApaimaneeClient

class ApaimaneeClientTest:
    def __init__(self):
        self.client = ApaimaneeClient()

    def login(self):

        response = self.client.user.login('aran@hotmail.com')
        print('login response: ', response)

    def register(self):

        response = self.client.user.register('Niniw', '12345', 'aran@hotmail.com', 'aran', 'khunaree')
        print('register response: ', response)

    def create_room(self):
        if not self.client.user.is_loggedin:
            self.login()

        user_id = self.client.user.get_user_id()

        response = self.client.room.create_room('AAA', user_id)
        print('creat room response: ', response)
        return response

    def join_game(self):
        create_room_response = self.create_room()
        response = self.client.room.join_game(create_room_response['room_id'], create_room_response['user_id'])
        print('join game response:', response)

    def status(self):
        print('controller status')

    def start(self):
        self.client.initial()
        commands = dict(
                login = self.login,
                register = self.register,
                create_room = self.create_room,
                join_game = self.join_game,
                start = self.status
                )
        while True:
            print('Please Mode command:1.login 2.register 3.create_room 4.join_game 5.start')
            cmd = input('Enter command :')

            func = commands.get(cmd, None)
            if func is not None:
                try:
                    func()
                except:
                    print('Error in function')


