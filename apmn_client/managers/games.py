
from .base import Manager

class GameManager(Manager):
    def __init__(self, client):
        super().__init__(client)
        room_id = self.client.room.current_room['room_id']
        self.topic = 'apaimanee/clients/{}/rooms/{}/update'.format(self.client.client_id, room_id)

    def send_message(self, method, args, qos=0):
        request = dict(room_id=room_id, method=method, args=args)

        self.client.publish(self.topic, request, qos)

    def ready(self):
        args = dict()
        self.send_message('ready', args, 1)

    def initial(self):
        args = dict()
        self.send_message('initial', args, 1)

    def update(self, **kw):
        args = kw
        self.send_message('update', args, 0)

    def move_hero(self, x, y):
        args = dict(x=x, y=y)
        self.send_message('move_hero', args)

    def skill_action(self, skill):
        args = dict(skill=skill)
        self.send_message('skill_action', args)
