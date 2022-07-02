#! python3.7

import paho.mqtt.client as mqtt 
from random import randrange, uniform, randint, choice
import threading, time, json, string, requests


TB_BASE_URL = "http://airva.local/api/v1" # Thingsboard

def startMQTT(broker):

    print("+ Send data to thingsboard")

    hostBroker = broker["host"]
    userBroker = broker["user"]
    passBroker = broker["pass"]
    portBroker = broker["port"]

    def server_on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.connected_flag = True
        
        client.subscribe('#')

    def server_on_message(client, userdata, msg):
        from_topic = msg.topic
        payload = str(msg.payload.decode())

        try:
            json_payload = json.loads(payload)
        except:
            json_payload = {}

        # # MQ135
        if from_topic == 'airva/device/esp8266mq123pp42ns' and len(json_payload) > 0:
            jObj = {
                "co2ppm" : json_payload["mq135"].get("co2ppm"), # CO2 * Não importante
                "statedetect" : json_payload["mq135"].get("statedetect"), # Valor analógico de detecão de gás,
                "raw" : json_payload["mq135"].get("raw"), # Valor bruto de CO2
                "ppm_acetone" : json_payload["mq135"].get("ppm_acetone"), # Valor de acetona poeira
            }
            r = requests.post(url = "{}/s4pq80zjveHEomG0VvvD/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )

        # # PPD42NS
        if from_topic == 'airva/device/esp8266mq123pp42ns' and len(json_payload) > 0:
            jObj = {
                "lowpulseoccupancy" : json_payload["ppd42ns"].get("lowpulseoccupancy"), # Concentração de poeira
                "ratio" : json_payload["ppd42ns"].get("ratio"), # Valor de radio
                "concentration" : json_payload["ppd42ns"].get("concentration") # Concentração de poeira
            }
            r = requests.post(url = "{}/TBYcHsHrETJOOfllx99D/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )

        # # T6615
        if from_topic == 'airva/device/esp8266co2' and len(json_payload) > 0:
            jObj = {
                "ppmco2" : json_payload.get("ppm_co2"), # CO2 
                "detect_co2" : json_payload.get("detect_co2"), # CO2 
            }
            r = requests.post(url = "{}/4qln5iCFzDghv5JzuenT/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )



        # ljtqY03RJdT1TaoM69xX
        if from_topic == 'airva/device/esp8266rgboledsht30' and len(json_payload) > 0:
            jObj = {
                "temperature" : json_payload.get("temperature"), # 
                "humidity" : json_payload.get("humidity"), # 
            }
            r = requests.post(url = "{}/ljtqY03RJdT1TaoM69xX/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )


        # ZIGBEE TO MQTT
        if from_topic == 'airva/device/esp8266rgboledsht30' and len(json_payload) > 0:
            jObj = {
                "temperature" : json_payload.get("temperature"), # 
            }
            r = requests.post(url = "{}/ljtqY03RJdT1TaoM69xX/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )


        # SONOFF_SNZB-02_TH1 - Temperature and humidity sensor (EndDevice)
        if from_topic == 'zigbee2mqtt/0x00124b0025045eca' and len(json_payload) > 0:
            jObj = {
                "temperature" : json_payload.get("temperature"),
                "humidity" : json_payload.get("humidity"),
                "battery" : json_payload.get("battery"),
            }
            r = requests.post(url = "{}/FmWv4ovXCJSWbg5T4ttF/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )
        
        # SONOFF_SNZB-02_TH2 - Temperature and humidity sensor (EndDevice)
        if from_topic == 'zigbee2mqtt/0x00124b00251c765c' and len(json_payload) > 0:
            jObj = {
                "temperature" : json_payload.get("temperature"),
                "humidity" : json_payload.get("humidity"),
                "battery" : json_payload.get("battery"),
            }
            r = requests.post(url = "{}/yl6fVVjKzfFjKkvArXSJ/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )

        # SONOFF_SNZB-04_CS1 - Contact sensor (EndDevice)
        if from_topic == 'zigbee2mqtt/0x00124b002512e998' and len(json_payload) > 0:
            contact = json_payload.get("contact")
            if contact: contact = 1
            else: contact = 0
            jObj = {
                "contact" : contact,
                "battery" : json_payload.get("battery"),
            }
            r = requests.post(url = "{}/u4xz49L4tphmlFIxh9Bb/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )

        # SONOFF_SNZB-03_MS - Motion sensor (EndDevice)
        if from_topic == 'zigbee2mqtt/0x00124b0025455781' and len(json_payload) > 0:
            occupancy = json_payload.get("occupancy")
            if occupancy: occupancy = 1
            else: occupancy = 0
            jObj = {
                "occupancy" : occupancy,
                "battery" : json_payload.get("battery"),
            }
            r = requests.post(url = "{}/3esximI4kXcVQRPR4SKp/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )

        # SONOFF_S26R2ZB_SP - Zigbee Smart Plug (Router)
        if from_topic == 'zigbee2mqtt/0x00124b0024c2aafd' and len(json_payload) > 0:
            state = json_payload.get("state")
            if state == "ON": state = 1
            else: state = 0
            jObj = {
                "state" : state,
            }
            r = requests.post(url = "{}/GfM5QuAE8UvLUE7fMP2t/telemetry".format(TB_BASE_URL), data = json.dumps(jObj) )


        
    server_client = mqtt.Client()
    server_client.username_pw_set(userBroker, passBroker)
    server_client.on_connect = server_on_connect
    server_client.on_message = server_on_message
    server_client.connect_async(hostBroker, portBroker, 60)
    server_client.loop_forever()


def init(argv):

    _broker = argv["broker"]

    func_threads = [
        [startMQTT, ([_broker])]
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1],)
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()