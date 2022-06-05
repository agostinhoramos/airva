#! python3.7

import paho.mqtt.client as mqtt
import threading, time, json

hostBroker = "127.0.0.1"
userBroker = "mqttadmin"
passBroker = "over224433"
portBroker = 1883

def server_on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
    
    topic_name = "zigbee2mqtt"
    print("Connected to your server with topic name '{}' ".format(topic_name))
    client.subscribe(topic_name + '/#')

def server_on_message(client, userdata, msg):
    from_topic = msg.topic
    payload = str(msg.payload.decode())

    print( payload )

server_client = mqtt.Client()
server_client.username_pw_set(userBroker, passBroker)
server_client.on_connect = server_on_connect
server_client.on_message = server_on_message
server_client.connect_async(hostBroker, portBroker, 60)
server_client.loop_forever()