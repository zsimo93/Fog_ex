import requests
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "bdb20650-54c0-4a48-b9b5-fc79bb57aee2",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "large"
        },
        "except": {
            "add2Str": {
                "actionClass": "large"
            }
        },
        "log": True
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s", json=payload)
    r.json["elapsed"] = r.elapsed
    print r.json


Thread(target=send).start()