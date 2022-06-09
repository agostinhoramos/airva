#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import time, json, string

class Mock():
    def __init__(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.device_id = ''.join(choice(letters) for i in range(8))
        self.sensor_type = 'esp8266node2'
        self.server_client = None
        self.battery_limit = 25
        self.battery_low = False
        self.topic = None

    def connect(self, name, broker, topic):
        self.server_client = mqtt.Client()
        self.server_client.username_pw_set(broker["user"], broker["pass"])
        self.server_client.connect(broker["host"], broker["port"], 60)
        self.topic = topic.replace("@sensor_type@", self.sensor_type)\
                          .replace("@device_id@", self.device_id)\
                          .replace("@device_name@", name)

    def run(self):
        battery_life = 100 # 0% to 100%
        contact_life = False

        while battery_life > 0:
            waitNext = uniform(3, 30)

            if battery_life > 0 and randint(1, 20) == 1:
                bty = uniform(0.10, 1.3)
                battery_life = (battery_life - bty)

            if int(battery_life) < self.battery_limit:
                self.battery_low = True

            payload = {
                "battery_low" : self.battery_low
            }
                
            self.server_client.publish(self.topic, json.dumps(payload))
            time.sleep(waitNext)

def init(name, mode, argv):
    # mode = normal|test|extreme
    mock = Mock()
    mock.connect(name, argv["broker"], argv["config"]["topic"])
    mock.run()