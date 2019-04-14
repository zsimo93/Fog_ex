import requests
import time
import fileModule, os
vidProc = "http://127.0.0.1:9001/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/video/process"
path = r'C:\Users\Simone\Desktop\tst\output000.ts'
def invoke(path=path):
    filename = os.path.basename(path)
    fm = fileModule.FileManager()
    begin = time.time()
    fin = open(path, "rb")
    id0 = fm.saveFile(fin.read(), filename)
    fin.close()

    payload = {"videoID": id0}
    resp = requests.post(vidProc, json=payload)

    vid = resp.json()["videoID"]
    file = open("local-out.ts", "wb")
    vidOut = fm.loadFile(vid)
    file.write(vidOut.read())
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
