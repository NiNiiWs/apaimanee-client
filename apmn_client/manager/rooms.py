
from .base import Manager

class RoomManager(Manager):
    def __init__(self, client):
        super().__init__(client)
        self.rooms = RoomManager

    def create_room(self, name_room):

        args = dict(name_room=name_room)
        response = self.call('create_room', args)
        return response

    def join_game(self, room_id):

        args = dict(room_id=room_id)

        response  = self.call('join_game', args)

        return response
