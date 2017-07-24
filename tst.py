import requests, time
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "c9b23b3c-9421-49e6-87c0-35e8c6544fcd",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "small"
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s4", json=payload)
    print r.elapsed
    print r.json()


for i in range(0, 3):
    Thread(target=send).start()
    Thread(target=send).start()
    time.sleep(60)