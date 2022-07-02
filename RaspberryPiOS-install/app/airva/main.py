#!/usr/bin/python3
import threading, time, json, sys, os

from dotenv import dotenv_values
_env = dotenv_values(".env.local")
sys.path.append( _env["ROOT_PATH"] )

from airva.backend import index as backend

from airva.middleware.systemController import index as systemController
from airva.middleware.sendDataToThingsboard import index as sendDataToThingsboard
from airva.middleware.watchDeviceEvents import index as watchDeviceEvents

argv = {
    "broker" : {
        "host" : "airva.local",
        "user" : "mqttadmin",
        "pass" : "over224433",
        "port" : 1883
    },
    "config" : {
        "topic" : "airva/device"
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
        # Start webpage
        # [backend.init, ([_])],

        # System controller
        [systemController.init, ([argv])],

        # Send data to thingsboard
        [sendDataToThingsboard.init, ([argv])],

        # Watch for new events
        [watchDeviceEvents.init, ([argv])],
    ]

    threads = []
    for fn in func_threads:
        th = threading.Thread(target=fn[0], args=fn[1], )
        th.start()
        threads.append(th)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print("\n*** Welcome to AirVa Service ***")
    main()