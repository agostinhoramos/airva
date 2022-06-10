#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import time, json, string

class Mock():
    def __init__(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.device_id = ''.join(choice(letters) for i in range(8))
        self.sensor_type = 'tmprt_hmdty'
        self.server_client = None
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
        temperature_live = 25 # 0.0º to 45.0º
        humidity_life = 54 # 0.0% to 100.0%

        while battery_life > 0:
            waitNext = uniform(3, 30)

            if battery_life > 0 and randint(1, 20) == 1:
                bty = uniform(0.10, 1.3)
                battery_life = (battery_life - bty)

            if randint(1, 3) == 1:
                tmp = uniform(0.10, 2.3)
                if randint(1, 4) == 1:
                    temperature_live = (temperature_live - tmp)
                else:
                    temperature_live = (temperature_live + tmp)

                if temperature_live > 32 or temperature_live < 12:
                    temperature_live = 32/2

            if randint(1, 3) == 1:
                hmd = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    humidity_life = (humidity_life - hmd)
                else:
                    humidity_life = (humidity_life + hmd)

                if humidity_life > 97 or humidity_life < 32:
                    humidity_life = 32/2

            payload = {
                "battery" : int(battery_life),
                "humidity" : float("{:.2f}".format(humidity_life)),
                "temperature" : float("{:.2f}".format(temperature_live))
            }
                
            self.server_client.publish(self.topic, json.dumps(payload))

            time.sleep(waitNext)


def init(name, mode, argv):
    # mode = normal|test|extreme
    mock = Mock()
    mock.connect(name, argv["broker"], argv["config"]["topic"])
    mock.run()