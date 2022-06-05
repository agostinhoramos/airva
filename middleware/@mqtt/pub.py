#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

hostBroker = "127.0.0.1"
userBroker = "mqttadmin"
passBroker = "over224433"
portBroker = 1883

server_client = mqtt.Client()
server_client.username_pw_set(userBroker, passBroker)
server_client.connect(hostBroker, portBroker, 60)

TOPIC = "demo/temperature"

while True:
    myValue = uniform(20.0, 21.0)

    server_client.publish(TOPIC, myValue)
    print("Just published " + str(myValue) + " to topic {}" .format(TOPIC))
    time.sleep(1)