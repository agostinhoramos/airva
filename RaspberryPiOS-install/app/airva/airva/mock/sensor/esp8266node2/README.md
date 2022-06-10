# ESP 8266 SENSOR - NODE 2


payload = {
    "sht30" : {
        "humidity" : 32,
        "temperature" : 21
    },
    "mq135" : {
        "rzero" : 0.0, # 63.08
        "crzero" : 0.0, # 62.33
        "resistance" : 0.0, # 39.90
        "ppm" : 0.0, # 710.31
        "cppm" : 0.0 # 734.27
    },
    "co2t6615" : {
        "co2" : "" # 0 - 2000
    },
    "dsm501a" : {
        "dust_level" : "CLEAN", # CLEAN|GOOD|ACCEPTABLE|HEAVY|HAZARD
    }
}