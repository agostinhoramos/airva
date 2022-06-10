#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import time, json, string

class Mock():
    def __init__(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.device_id = ''.join(choice(letters) for i in range(8))
        self.topic = None
        self.payload = {}
        self.LIFE = {}
        self.MARGIN = {}
        self.changed = False
        self.sensor_type = 'esp8266node2'
        self.server_client = None

        self.battery_limit = 25

    def connect(self, name, broker, topic):
        self.server_client = mqtt.Client()
        self.server_client.username_pw_set(broker["user"], broker["pass"])
        self.server_client.connect(broker["host"], broker["port"], 60)
        self.topic = topic.replace("@sensor_type@", self.sensor_type)\
                          .replace("@device_id@", self.device_id)\
                          .replace("@device_name@", name)

    def run(self):
        dust_level = ["CLEAN", "GOOD", "ACCEPTABLE", "HEAVY", "HAZARD"]
        _temperature = 12
        self.LIFE = {
            "battery" : 100, # 0% to 100%
            "temperature" : 45/2, # 0.0º to 45.0º
            "humidity" : 100/2, # 0.0% to 100.0%
            "rzero" : 63.08/2, # 63.08
            "crzero" : 62.33/2, # 62.33
            "resistance" : 39.90/2, # 39.90
            "ppm" : 710.31/2, # 710.31
            "cppm" : 734.27/2, # 734.27
            "co2" : 1500/2, # 0 - 2000
            "dust_level" : 1, # CLEAN|GOOD|ACCEPTABLE|HEAVY|HAZARD
        }
        
        # Define value
        self.payload = {
            "battery_low" : None,
            "sht30" : {},
            "mq135" : {},
            "co2t6615" : {},
            "dsm501a" : {}
        }

        while self.LIFE["battery"] > 0:
            self.changed = False

            waitNext = uniform(1, 3)

            if self.LIFE["battery"] > 0 and randint(1, 20) == 1:
                bty = uniform(0.10, 1.3)
                self.LIFE["battery"] = (self.LIFE["battery"] - bty)

            self.payload.update({"battery_low":False})
            if int(self.LIFE["battery"]) < self.battery_limit:
                self.payload.update({"battery_low":True})
                self.changed = True
                
            if randint(0, 1) == 1:
                tmp = uniform(0.10, 2.3)
                if randint(0, 1) == 1:
                    self.LIFE["temperature"] = (self.LIFE["temperature"] - tmp)
                else:
                    self.LIFE["temperature"] = (self.LIFE["temperature"] + tmp)

                # Define limit
                if self.LIFE["temperature"] > 32 or self.LIFE["temperature"] < 12:
                    self.LIFE["temperature"] = 45/2

                self.payload["sht30"].update({"temperature": float("{:.2f}".format(self.LIFE["temperature"])) })
                self.changed = True

            if randint(0, 1) == 1:
                hmd = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["humidity"] = (self.LIFE["humidity"] - hmd)
                else:
                    self.LIFE["humidity"] = (self.LIFE["humidity"] + hmd)

                # Define limit
                if self.LIFE["humidity"] > 87 or self.LIFE["humidity"] < 35:
                    self.LIFE["humidity"] = 100/2

                self.payload["sht30"].update({"humidity": float("{:.2f}".format(self.LIFE["humidity"])) })
                self.changed = True

            if randint(0, 1) == 1:
                rzero = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["rzero"] = (self.LIFE["rzero"] - rzero)
                else:
                    self.LIFE["rzero"] = (self.LIFE["rzero"] + rzero)

                # Define limit
                if self.LIFE["rzero"] > 120 or self.LIFE["rzero"] < 50:
                    self.LIFE["rzero"] = 63.08/2

                self.payload["mq135"].update({"rzero": float("{:.2f}".format(self.LIFE["rzero"])) })
                self.changed = True

            if randint(0, 1) == 1:
                crzero = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["crzero"] = (self.LIFE["crzero"] - crzero)
                else:
                    self.LIFE["crzero"] = (self.LIFE["crzero"] + crzero)

                # Define limit
                if self.LIFE["crzero"] > 120 or self.LIFE["crzero"] < 50:
                    self.LIFE["crzero"] = 63.08/2
                
                self.payload["mq135"].update({"crzero": float("{:.2f}".format(self.LIFE["crzero"])) })
                self.changed = True

            if randint(0, 1) == 1:
                resistance = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["resistance"] = (self.LIFE["resistance"] - resistance)
                else:
                    self.LIFE["resistance"] = (self.LIFE["resistance"] + resistance)

                # Define limit
                if self.LIFE["resistance"] > 120 or self.LIFE["resistance"] < 24:
                    self.LIFE["resistance"] = 39.90/2

                self.payload["mq135"].update({"resistance": float("{:.2f}".format(self.LIFE["resistance"])) })
                self.changed = True

            if randint(0, 1) == 1:
                ppm = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["ppm"] = (self.LIFE["ppm"] - ppm)
                else:
                    self.LIFE["ppm"] = (self.LIFE["ppm"] + ppm)

                # Define limit
                if self.LIFE["ppm"] > 1430 or self.LIFE["ppm"] < 204:
                    self.LIFE["ppm"] = 710.31/2

                self.payload["mq135"].update({"ppm": float("{:.2f}".format(self.LIFE["ppm"])) })
                self.changed = True

            if randint(0, 1) == 1:
                cppm = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["cppm"] = (self.LIFE["cppm"] - cppm)
                else:
                    self.LIFE["cppm"] = (self.LIFE["cppm"] + cppm)

                # Define limit
                if self.LIFE["cppm"] > 1430 or self.LIFE["cppm"] < 204:
                    self.LIFE["cppm"] = 734.27/2

                self.payload["mq135"].update({"cppm": float("{:.2f}".format(self.LIFE["cppm"])) })
                self.changed = True

            if randint(0, 1) == 1:
                co2 = uniform(0.23, 4.3)
                if randint(1, 4) == 1:
                    self.LIFE["co2"] = (self.LIFE["co2"] - co2)
                else:
                    self.LIFE["co2"] = (self.LIFE["co2"] + co2)

                # Define limit
                if self.LIFE["co2"] > 2330 or self.LIFE["co2"] < 404:
                    self.LIFE["co2"] = 1500/2

                self.payload["co2t6615"].update({"co2": float("{:.2f}".format(self.LIFE["co2"])) })
                self.changed = True

            if randint(0, 1) == 1:
                dl = randint(0, 4)
                self.payload["dsm501a"].update({"dust_level": dust_level[dl] })
                self.changed = True
            
            if self.changed:
                self.server_client.publish(self.topic, json.dumps(self.payload))

            time.sleep(waitNext)

def init(name, mode, argv):
    # mode = normal|test|extreme
    mock = Mock()
    mock.connect(name, argv["broker"], argv["config"]["topic"])
    mock.run()