import requests, time
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "50faf500-3e7a-4b0e-b447-192ada6f9332",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "small"
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s4", json=payload)
    print r.elapsed
    print r.json()


for i in range(0, 20):
    Thread(target=send).start()
