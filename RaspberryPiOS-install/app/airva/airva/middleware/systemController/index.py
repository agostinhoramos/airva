#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import threading, time, json, string, requests


TB_BASE_URL = "http://airva.local/api/v1" # Thingsboard

def startMQTT(broker):

    print("+ Enable system controller")

    hostBroker = broker["host"]
    userBroker = broker["user"]
    passBroker = broker["pass"]
    portBroker = broker["port"]

    def server_on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
        
        client.subscribe('airva/device/#')

    def server_on_message(client, userdata, msg):
        from_topic = msg.topic
        payload = str(msg.payload.decode())

        try:
            json_payload = json.loads(payload)
        except:
            json_payload = None

        # ESP8266_OCCUPANTSCOUNTER
        if 'esp8266_occupantscounter0x01' in from_topic and json_payload != None:
            occupants = json_payload
            
            semaphore = 1
            if occupants >= 50:
                semaphore = 3
                server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "ON"}))
            elif occupants >= 25:
                semaphore = 2
            else:
              server_client.publish('zigbee2mqtt/0x00124b0024c2aafd/set', json.dumps({"state": "OFF"}))

            payload = json.dumps({ "occupants" : occupants, "semaphore" : semaphore })
            server_client.publish('airva/device/esp8266_display0x01/set', payload)


    server_client = mqtt.Client()
    server_client.username_pw_set(userBroker, passBroker)
    server_client.on_connect = server_on_connect
    server_client.on_message = server_on_message
    server_client.connect_async(hostBroker, portBroker, 60)
    server_client.loop_forever()


def init(argv):

    _broker = argv["broker"]

    func_threads = [
        [startMQTT, ([_broker])]
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1],)
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()