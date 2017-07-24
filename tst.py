import requests
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "b75b2009-d47a-413a-8c96-e8b760b033e9",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "large"
        },
        "except": {
            "add2Str": {
                "actionClass": "large"
            }
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s4", json=payload)
    print r.elapsed
    print r.json()


for i in range(0,20):
    Thread(target=send).start()