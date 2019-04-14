import time
import requests
from threading import Thread
import fileModule
import os

resize = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/image/resize"
bw = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/image/bw"
compose = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/image/compose"
rotate = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/image/rotate"
grey = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/image/grey"

path=r'C:\Users\Simone\Desktop\tst\Star-Wars.png'

class CallerThread(Thread):
    def __init__(self, path, payload):
        self.path = path
        self.payload = payload
        Thread.__init__(self)

    def run(self):
        r = requests.post(self.path, json=self.payload)

        self.ret = r.json()


def invoke(path=path):
    filename = os.path.basename(path)
    fm = fileModule.FileManager()
    begin = time.time()
    fin = open(path, "rb")
    id0 = fm.saveFile(fin.read(), filename)
    payload = {"id": id0, "formatOut": "PNG"}
    resp = requests.post(resize, json=payload)
    r = resp.json()
    id1 = r["retId"]

    payload = {"id": id1, "formatOut": "PNG"}
    bwT = CallerThread(bw, payload)
    bwT.start()
    rotateT = CallerThread(rotate, payload)
    rotateT.start()
    greyT = CallerThread(grey, payload)
    greyT.start()

    bwT.join()
    id2 = bwT.ret["retId"]

    rotateT.join()
    id3 = rotateT.ret["retId"]

    greyT.join()
    id4 = greyT.ret["retId"]

    payload = {
        "id1": id1,
        "id2": id2,
        "id3": id3,
        "id4": id4
    }
    resp = requests.post(compose, json=payload)

    idOut = resp.json()["retId"]
    buff = fm.loadFile(idOut)
    file = open("local-out.png", "wb")
    file.write(buff.read())
    file.close()
    elapsed = time.time() - begin
    print elapsed
    return elapsed


def run():
    one = open("one-no", "w")

    for i in range(0, 20):
        num = invoke()
        one.write(repr(num) + "\n")
        time.sleep(1)

    one.close()
