#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import threading, time, json, string

class Mock():
    def __init__(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.device_id = ''.join(choice(letters) for i in range(8))
        self.topic = None
        self.payload = {}
        self.changed = False
        self.sensor_type = 'esp8266node1'
        self.server_client = None

        self.battery_limit = 25
        self.battery_low = False

        # modules
        self.oled_shield = {}
        self.rgb_led = {}

    def connect(self, name, broker, topic):
        self.server_client = mqtt.Client(self.device_id)
        self.server_client.username_pw_set(broker["user"], broker["pass"])
        self.server_client.connect(broker["host"], broker["port"], 60)
        self.topic = topic.replace("@sensor_type@", self.sensor_type)\
                          .replace("@device_id@", self.device_id)\
                          .replace("@device_name@", name)

    def run(self):
        battery_life = 100 # 0% to 100%
        contact_life = False
        self.payload = {
            "battery_low" : False,
            "count_detect" : 0
        }

        while battery_life > 0:
            waitNext = uniform(3, 7)

            if battery_life > 0 and randint(1, 20) == 1:
                bty = uniform(0.10, 1.3)
                battery_life = (battery_life - bty)

            if int(battery_life) < self.battery_limit:
                self.battery_low = True
                self.payload.update( {"battery_low" : self.battery_low } )

            if randint(1, 2) == 1:

                result = (self.payload["count_detect"] + 1)
                if randint(1, 2) == 1:
                    if self.payload["count_detect"] > 0:
                        result = (self.payload["count_detect"] - 1)

                self.payload.update( 
                    {
                        "count_detect": result
                    } 
                )
                
            self.server_client.publish(self.topic, json.dumps(self.payload))
            time.sleep(waitNext)

    def watch(self):
        def server_on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.connected_flag = True

            client.subscribe(self.topic + '/set')

        def server_on_message(client, userdata, msg):
            from_topic = msg.topic
            payload = str(msg.payload.decode())
            pjson = json.loads(payload)

            count_detect = pjson.get("count_detect")
            if count_detect:
                if count_detect.get("ack") == self.payload["count_detect"]:
                    self.payload["count_detect"] = 0
            
            oled_shield = pjson.get("oled_shield")
            if oled_shield:
                self.oled_shield = oled_shield
                print("OLED: ", self.oled_shield.get("text"))

            rgb_led = pjson.get("rgb_led")
            if rgb_led:
                self.rgb_led = rgb_led
                print("RGB_LED: ", self.rgb_led.get("color"))

        self.server_client.on_connect = server_on_connect
        self.server_client.on_message = server_on_message
        self.server_client.loop_forever()

def init(name, mode, argv):
    # mode = normal|test|extreme
    mock = Mock()
    mock.connect(name, argv["broker"], argv["config"]["topic"])

    func_threads = [
        [mock.run, ([])],
        [mock.watch, ([])]
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1],)
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()