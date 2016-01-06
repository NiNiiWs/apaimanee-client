
from .base import Manager

class RoomManager(Manager):
    def __init__(self, client):
        super().__init__(client)
        self.rooms = RoomManager

    def create_room(self, name_room):
        print("Create Room")
        args = dict(name_room=name_room)

        response = self.call('create_room', args)
        if 'room_id' in response['responses']:

            self.client.gm.start_game(response['responses']['room_id'])

        return response

    def join_game(self, room_id):
        print("Join Game")
        args = dict(room_id=room_id)

        response  = self.call('join_game', args)
        if not self.client.gm.is_running():
            if 'room_id' in response['responses']:
                self.client.gm.start_game(response['responses']['room_id'])

        return response
