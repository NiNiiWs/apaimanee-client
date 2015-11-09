
from . import UserManager

class RoomManager(UserManager):
    def __init__(self, client):
        self.client = client
        self.rooms = RoomManager

    def create_room(self, name_room, user_id):
        args = dict(name_room=name_room,
                user_id=user_id,
                method='create_room')
        response = self.client.call(args)

        return response
