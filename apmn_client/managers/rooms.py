
from .base import Manager

class RoomManager(Manager):
    def __init__(self, client):
        super().__init__(client)
        self.current_room = None

    def create_room(self, room_name):
        print("Create Room")
        args = dict(room_name = room_name)

        response = self.call('create_room', args)
        if 'room_id' in response['responses']:
            self.join_game(response['responses']['room_id'])
        #    self.client.gm.start_game(response['responses']['room_id'])
        return response

    def join_game(self, room_id):
        print("Join Game")
        args = dict(room_id=room_id)

        response  = self.call('join_game', args)
        if not self.client.gm.is_running():
            if 'room_id' in response['responses']:
                self.client.gm.start_game(response['responses']['room_id'])

        self.current_room = args
        return response

    def list_rooms(self):
        args = dict()
        response = self.call('list_rooms', args)

        return response

    def list_players(self):
        args = dict(room_id=self.current_room['room_id'])
        response = self.call('list_players', args)

        return response

    def select_hero(self, hero):
        args = dict(hero=hero, room_id=self.current_room['room_id'])
        response =self.call('select_hero', args)
        return response
