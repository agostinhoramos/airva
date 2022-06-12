#! python3.8
import sys, time, json
import paho.mqtt.client as mqtt

sys.path.append(".")
from lib.data.broker import json_broker

def publish(username, password, payload, forever = False):
    mqtt.Client.connected_flag = False
    mqtt.Client.suppress_puback_flag = False
    client = mqtt.Client()

    def on_log(client, userdata, level, buf):
        print(buf) 

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
        else:
            print("Bad connection Returned code = ", rc)
        client.loop_stop()

    def on_publish(client, userdata, mid):
        print("> Published in Thingsboard : {}".format(mid))

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.publish("v1/devices/me/telemetry", payload, 1)

    client.username_pw_set(username, password)
    client.connect("airva.local", 1553)

    if forever:
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            client.disconnect()
    else:
        try:
            repeat = 0
            while repeat < 3:
                client.loop()
                repeat += 1
        except KeyboardInterrupt:
            client.disconnect()

def subscribe(topic):
    pass