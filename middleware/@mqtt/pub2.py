#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time, json

hostBroker = "127.0.0.1"
userBroker = "mqttadmin"
passBroker = "over224433"
portBroker = 1883

server_client = mqtt.Client()
server_client.username_pw_set(userBroker, passBroker)
server_client.connect(hostBroker, portBroker, 60)

TOPIC = "zigbee2mqtt/mysmart_plug/set"

myValue = json.dumps({"state": "TOGGLE"})

server_client.publish(TOPIC, myValue)