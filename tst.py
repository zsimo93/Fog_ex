import requests, time
from threading import Thread

def send():
    payload = {
        "param": {
            "id": "ee7345fc-afaf-4601-a827-a90bb15d0ab1",
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "large"
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s3", json=payload)
    print r.elapsed
    print r.json()


for i in range(0, 20):
    Thread(target=send).start()
