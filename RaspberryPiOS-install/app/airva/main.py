#!/usr/bin/python3
import threading, time, json, sys, os

from dotenv import dotenv_values
_env = dotenv_values(".env.local")
sys.path.append( _env["ROOT_PATH"] )

from airva.backend import index as backend
from airva.mock.sensor.stmphum24 import init as mock__stmphum24
from airva.mock.sensor.contactsn04 import init as mock__contactsn04

from airva.mock.sensor.esp8266node1 import init as mock__esp8266node1
from airva.mock.sensor.esp8266node2 import init as mock__esp8266node2

argv = {
    "broker" : {
        "host" : "127.0.0.1",
        "user" : "mqttadmin",
        "pass" : "over224433",
        "port" : 1883
    },
    "config" : {
        "topic" : "airva/device/@sensor_type@/@device_name@"
    }
}

def main():
    _ = "DEV"
    if _env["PROD_MOD"] == '1':
        _ = "PRD"

    if os.geteuid() == 0:
        print("Running as ROOT :)")

    ## RUN ALL THREADS ##
    func_threads = [
        #[backend.init, ([_])],

        # ESP
        [mock__esp8266node1.init, (["oledcountrgb", "normal", argv])],
        [mock__esp8266node2.init, (["tmphmdco2dsm", "normal", argv])],

        # SONOFF
        [mock__stmphum24.init, (["sonoff_th_1", "normal", argv])],
        [mock__contactsn04.init, (["sonoff_cnct_windows", "normal", argv])],
        [mock__contactsn04.init, (["sonoff_cnct_door", "normal", argv])],
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1], )
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("Server running..")
    main()
    