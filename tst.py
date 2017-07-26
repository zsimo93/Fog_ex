import requests, time
from threading import Thread
import sys

def send(id):
    payload = {
        "param": {
            "id": id,
            "text": "RANDOM TEXT!!!"},
        "default": {
            "actionClass": "small"
        },
        "log": False
    }

    r = requests.post("http://192.168.1.50:8080/api/invoke/s2", json=payload)
    print r.elapsed
    print r.json()
n = int(sys.argv[1])
for i in range(0, n):
    Thread(target=send, args=(sys.argv[2],)).start()
