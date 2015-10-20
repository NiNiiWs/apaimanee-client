import paho.mqtt.client as mqttclient
import json

import uuid
import time
import datetime
import threading

from . import callbacks
from . import manager

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("apaimanee/#")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic+" "+json.dumps(payload))


class RPC:
    def __init__(self):
        self.response = dict()

    def check_response(self, request_id):
        return request_id in self.response

    def get_response(self, request_id):
        if self.check_response(request_id):
            return self.response.pop(request_id)
        return None

    def rpc_response(self, client, rpc, msg):
        payload = json.loads(msg.payload.decode('utf-8'))

        print("get response:", payload)
        if 'message_id' in payload:
            rpc.response[payload['message_id']] = payload


class ConsumeThread(threading.Thread):
    def __init__(self, mqtt_client):
        super().__init__()

        self.mqtt_client = mqtt_client
        self.deamon = True

    def run(self):

        try:
            self.mqtt_client.loop_forever()
        except Exception as e:
            print('Exception:', e)
        finally:
            self.mqtt_client.disconnect()

class ApaimaneeClient:
    def __init__(self):

        self.client_id = str(uuid.uuid1())

        self.mqtt_client = mqttclient.Client(self.client_id,
                clean_session=False)

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message


        self.rpc = RPC()
        self.mqtt_client.user_data_set(self.rpc)

        self.user = manager.UserManager(self)
        # add adition manager


    def initial(self):
        self.reconnect()
        self.consume_thread = ConsumeThread(self.mqtt_client)
        self.consume_thread.start()

    def reconnect(self):
        self.mqtt_client.connect("localhost", 1883, 60)
        #self.mqtt_client.subscribe('apaimanee/clients/#')
        self.register_callback()

    def register_callback(self):
        print('regist:', 'apaimanee/clients/'+self.client_id+'/response')
        self.mqtt_client.message_callback_add('apaimanee/clients/'+self.client_id+'/response',
                self.rpc.rpc_response)
        #self.mqtt_client.message_callback_add('apaimanee/status', callbacks.status)


    def publish(self, topic, args=None):
        if args is None:
            args = dict()

        args['client_id'] = self.client_id
        payload = json.dumps(args)

        print('topic:', topic,'publish:', payload,)
        self.mqtt_client.publish(topic, payload)


    def call(self, args):
        message_id = str(uuid.uuid4())
        if args is None:
            args = dict()

        args['message_id'] = message_id
        self.publish('apaimanee/clients/request', args)

        started_date = datetime.datetime.now()
        while not self.rpc.check_response(message_id):
            time.sleep(0.01)
            print('wait for response')
            if datetime.datetime.now() - started_date > datetime.timedelta(seconds=2):
                raise Exception('RPC ERRPOR TIMEOUT')

        return self.rpc.get_response(message_id)


