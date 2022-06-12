import paho.mqtt.client as paho
import os
import json
import time
from datetime import datetime

ACCESS_TOKEN = "LdL8RB48Qtg9Bol6PIET"
hostBroker = "airva.local"
portBroker = 1553

def on_publish(client,userdata,result):
    print("data published to thingsboard \n")
    pass

server_client = paho.Client()
server_client.on_publish = on_publish
server_client.username_pw_set(ACCESS_TOKEN)
server_client.connect(hostBroker, portBroker, keepalive=60)

time.sleep(0.1)
payload = json.dumps({"temperature": 31.22})
server_client.publish("v1/devices/me/telemetry", payload)