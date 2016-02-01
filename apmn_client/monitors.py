
import threading
import time
import json


class GameMonitor(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.daemon = True
        self._running = False
        self._sleep_time = 1
        self.client = client
        self.mqtt_client = client.mqtt_client

        self.subscribe_topic = None
        self.publish_topic = None
        self.room_id = None

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False

    def start_game(self, room_id):

        self._running = True
        self.room_id = room_id
        self.subscribe_topic = 'apaimanee/clients/{}/rooms/{}/synchronize'.format(self.client.client_id, room_id)
        self.publish_topic = 'apaimanee/clients/{}/rooms/{}/update'.format(self.client.client_id, room_id)

        self.mqtt_client.message_callback_add(self.subscribe_topic, self.on_game_message)
        self.start()

    def on_game_message(self, client, userdata, msg):
        game_msg = json.loads(msg.payload.decode('utf-8'))

        # add update game message here
        print("gm got:",msg.topic, game_msg)

    def stop_game(self):
        self.stop()
        self.room_id = None
        self.subscribe_topic = None
        self.publish_topic = None

        self.mqtt_client.unsubscribe(self.subscribe_topic)

    def run(self):
        while(self._running):
            msg = dict(game={}, method='update_game_status', room_id=self.room_id, token=self.client.user.get_token())
            msg_json = json.dumps(msg)
            self.mqtt_client.publish(self.publish_topic, msg_json)

            time.sleep(self._sleep_time)
