#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import threading, time, json, string, requests



TB_BASE_URL = "http://airva.local/api/v1"

class Current():
    def __init__(self):
        self.statedetect = None
        self.event1 = False
        self.server_client = None
        self.occupants = 0


current = Current()

def currentValeuMQTT():

    hostBroker = "127.0.0.1"
    userBroker = "mqttadmin"
    passBroker = "over224433"
    portBroker = 1883

    def server_on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True

        client.subscribe('#')

    def server_on_message(client, userdata, msg):
        from_topic = msg.topic
        payload = str(msg.payload.decode())

        try:
            json_payload = json.loads(payload)
        except:
            json_payload = {}

        # 1
        if from_topic == 'airva/device/esp8266mq123pp42ns' and len(json_payload) > 0:
            current.statedetect = json_payload["mq135"].get("statedetect")
            print( current.statedetect )

        # 2
        if from_topic == 'airva/device/esp8266_occupantscounter0x01/occupants':
            current.occupants = json_payload
            print( current.occupants )

        
    server_client = mqtt.Client()
    server_client.username_pw_set(userBroker, passBroker)
    server_client.on_connect = server_on_connect
    server_client.on_message = server_on_message
    server_client.connect_async(hostBroker, portBroker, 60)
    server_client.loop_forever()

def eventTimer():
    while True:
        if current.event1:
            time.sleep(15)
            if current.statedetect == 0:
                payload = json.dumps({"state": "ON"})
                current.server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', payload)
                payload = json.dumps({ "occupants" : current.occupants, "semaphore" : 3 })
                current.server_client.publish('airva/device/esp8266_display0x01/set', payload)
            if current.statedetect > 0:
                payload = json.dumps({"state": "OFF"})
                current.server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', payload)
                payload = json.dumps({ "occupants" : current.occupants, "semaphore" : 1 })
                current.server_client.publish('airva/device/esp8266_display0x01/set', payload)

def startMQTT():

    print("+ Watch for device events ")

    hostBroker = "127.0.0.1"
    userBroker = "mqttadmin"
    passBroker = "over224433"
    portBroker = 1883

    def server_on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True

        current.server_client = server_client
        client.subscribe('#')

    def server_on_message(client, userdata, msg):
        from_topic = msg.topic
        payload = str(msg.payload.decode())

        try:
            json_payload = json.loads(payload)
        except:
            json_payload = {}


        # Case Example 1: If you open the door, the light turn on else turn off
        if from_topic == 'zigbee2mqtt/0x00124b002512e998' and len(json_payload) > 0:
            if not json_payload.get("contact"):
                server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "ON"}))
            else:
                server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "OFF"}))

        # Case Example 2: If the temperature reaches a certain limit of 28.5ºC turn on the air conditioning else turn off.
        if from_topic == 'zigbee2mqtt/0x00124b0025045eca' and len(json_payload) > 0:
            temperature = json_payload.get("temperature")
            if temperature > 28.5:
                server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "ON"}))
            else:
                server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "OFF"}))

        # Case Example 3: If
        if from_topic == 'airva/device/esp8266mq123pp42ns' and len(json_payload) > 0:
            statedetect = json_payload["mq135"].get("statedetect")
            if statedetect == 0:
                payload = json.dumps({ "occupants" : current.occupants, "semaphore" : 2 })
                server_client.publish('airva/device/esp8266_display0x01/set', payload)
                current.event1 = True
            else: 
                current.event1 = False
        
    server_client = mqtt.Client()
    server_client.username_pw_set(userBroker, passBroker)
    server_client.on_connect = server_on_connect
    server_client.on_message = server_on_message
    server_client.connect_async(hostBroker, portBroker, 60)
    server_client.loop_forever()


def init(argv):

    func_threads = [
        [startMQTT, ([])],
        [currentValeuMQTT, ([])],
        [eventTimer, ([])],
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1],)
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()