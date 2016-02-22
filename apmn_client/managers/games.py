
from .base import Manager

class GameManager(Manager):
    def __init__(self, client):
        super().__init__(client)

    def update(self, method, args):
        room_id = self.client.room.current_room['room_id']
        topic = 'apaimanee/clients/{}/rooms/{}/update'.format(self.client.client_id, room_id)
        request = dict(room_id=room_id, method=method, args=args)

        self.client.publish(topic, request)

    def ready(self):
        args = dict()
        self.update('ready', args)

    def initial(self):
        args = dict()
        self.update('initial', args)

    def move_hero(self, x, y):
        args = dict(x=x, y=y)
        self.update('move_hero', args)

