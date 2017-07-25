import requests, time
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "a6225083-bc26-4b3f-b6e1-9188c9c5d13f",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "large"
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s4", json=payload)
    print r.elapsed
    print r.json()


for i in range(0, 20):
    Thread(target=send).start()
