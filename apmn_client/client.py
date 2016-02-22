import paho.mqtt.client as mqttclient
import json

import uuid
import time
import datetime
import threading

from . import callbacks
from . import managers
from . import monitors

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe('apaimanee/clients/{}/#'.format(client._client_id))


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic+" got "+json.dumps(payload))


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
        self.running = True

    def stop(self):
        self.running = False
        self.mqtt_client.disconnect()

    def run(self):

        try:
            self.mqtt_client.loop_forever()
        except Exception as e:
            print('Exception:', e)
        finally:
            self.mqtt_client.disconnect()

class ApaimaneeClient:
    def __init__(self, client_id=None, host='localhost', port=1883):

        if client_id:
            self.client_id = client_id
        else:
            self.client_id = str(uuid.uuid1())
            print('uuid:', self.client_id)

        self._host = host
        self._port = port

        self.mqtt_client = mqttclient.Client(self.client_id,
                clean_session=False)

        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message


        self.rpc = RPC()
        self.mqtt_client.user_data_set(self.rpc)

        # add adition manager
        self.user = managers.UserManager(self)
        self.room = managers.RoomManager(self)
        self.game = managers.GameManager(self)
        self.gm = None
        self.consume_thread = None


    def initial(self):
        self.reconnect()
        self.consume_thread = ConsumeThread(self.mqtt_client)
        self.consume_thread.start()

    def reconnect(self):
        print('connnect to api:', self._host, ' port:', self._port)
        self.mqtt_client.connect(self._host, self._port, 60)
        #self.mqtt_client.subscribe('apaimanee/clients/#')
        self.register_callback()
        self.gm = monitors.GameMonitor(self)

    def disconnect(self):
        if self.consume_thread:
            self.consume_thread.stop()
        if self.gm:
            self.gm.stop()

    def register_callback(self):
        print('regist:', 'apaimanee/clients/'+self.client_id+'/response')
        self.mqtt_client.message_callback_add('apaimanee/clients/'+self.client_id+'/response',
                self.rpc.rpc_response)

    def publish(self, topic, request, qos=1, retain=False):

        request['client_id'] = self.client_id

        if self.user.is_loggedin():
            request['token'] = self.user.get_token()

        payload = json.dumps(request)

        print('topic:', topic,'publish:', payload,)
        self.mqtt_client.publish(topic, payload, qos, retain)


    def call(self, method, args=None):
        message_id = str(uuid.uuid4())
        request = dict()

        request['message_id'] = message_id

        request['method'] = method
        request['args'] = args
        request['status'] = 'request'
        self.publish('apaimanee/clients/request', request, 1)

        started_date = datetime.datetime.now()
        while not self.rpc.check_response(message_id):
            time.sleep(0.01)
            print('wait for response')
            if datetime.datetime.now() - started_date > datetime.timedelta(seconds=2):
                raise Exception('RPC ERRPOR TIMEOUT')

        return self.rpc.get_response(message_id)


