#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import threading, time, json, string, requests


class ThingsboardHTTP():
    def __init__(self, url, *args, **kwargs):
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.host = url
        self.token = None

    def setDevice(self, token):
        self.token = token

    def pub(self, data):
        url = '{}/api/v1/{}/telemetry'.format(self.host, self.token)
        r = requests.post(url, data=json.dumps(data), headers=self.headers)


class Mock():
    def __init__(self, *args, **kwargs):
        letters = string.ascii_lowercase
        self.device_id = ''.join(choice(letters) for i in range(8))
        self.topic = None
        self.payload = {}
        self.changed = False
        self.server_client = None
        self.tb_http = None

        self.battery_limit = 25
        self.battery_low = False

        # modules
        self.oled_shield = {}
        self.rgb_led = {}

    def connect(self, broker, topic):
        self.server_client = mqtt.Client(self.device_id)
        self.server_client.username_pw_set(broker["user"], broker["pass"])
        self.server_client.connect(broker["host"], broker["port"], 60)
        self.topic = topic

        self.tb_http = ThingsboardHTTP('http://airva.local')
        self.tb_http.setDevice('Z2jJ5PHzDfAebrOsWYal')

    def run(self):
        self.payload = {
            "battery_low" : False,
            "count_detect" : 0
        }
        # while True:
        #     self.payload.update( 
        #         {
        #             "count_detect": "result"
        #         } 
        #     )
        #     self.server_client.publish(self.topic, json.dumps(self.payload))
        #     time.sleep(3)

    def watch(self):
        def server_on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.connected_flag = True

            client.subscribe(self.topic + '/#')

        def server_on_message(client, userdata, msg):
            from_topic = msg.topic
            payload = str(msg.payload.decode())
            pjson = json.loads(payload)

            if 'device/esp8266node2' in from_topic:
                print(pjson)

                tmp = pjson.get('sht30').get('temperature')
                hmd = pjson.get('sht30').get('humidity')

                payload = {
                    "temperature" : tmp,
                    "humidity" : hmd
                }
                self.tb_http.setDevice('Z2jJ5PHzDfAebrOsWYal')
                self.tb_http.pub(payload)
            
            if 'device/esp8266node1' in from_topic:
                print(pjson)

                cnt = pjson.get('count_detect')

                payload = {
                    "count_detect" : cnt,
                }
                self.tb_http.setDevice('iJyxZP2nZpGWNF5H8hl7')
                self.tb_http.pub(payload)

            if 'device/tmprt_hmdty/sonoff_th_1' in from_topic:
                print(pjson)

                tmp = pjson.get('temperature')
                hmd = pjson.get('humidity')

                payload = {
                    "temperature" : tmp,
                    "humidity" : hmd
                }

                self.tb_http.setDevice('TQagswhkY2lkQLLi3Xfg')
                self.tb_http.pub(payload)

            if 'device/mgntc_cnct/sonoff_cnct_windows' in from_topic:
                print(pjson)

                cnt = pjson.get('contact')

                payload = {
                    "contact" : cnt
                }

                self.tb_http.setDevice('8uQ298tS2idwI6S32bf9')
                self.tb_http.pub(payload)

            if 'device/mgntc_cnct/sonoff_cnct_door' in from_topic:
                print(pjson)

                cnt = pjson.get('contact')

                payload = {
                    "contact" : cnt
                }

                self.tb_http.setDevice('wBzF6wX1LJyvsTIj9xUn')
                self.tb_http.pub(payload)

        self.server_client.on_connect = server_on_connect
        self.server_client.on_message = server_on_message
        self.server_client.loop_forever()

def init(argv):
    mock = Mock()
    mock.connect(argv["broker"], argv["config"]["topic"])

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