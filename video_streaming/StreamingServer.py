from flask import Flask, make_response, request
import os
from pythonlib import connectionManager
import subprocess
from threading import Thread
from time import sleep

app = Flask(__name__)
cm = connectionManager.ConnectionManager("192.168.1.50")
targetPlayingAddress = "192.168.1.4:1234"

def playlistFile(name, stream):
    path = os.path.join(name, stream, "playlist.txt")
    f = open(path, "w+")

    str = ""
    for i in range(0, 400):
        str += "file '.\\%s\\%s\\output%03d.ts'\n" % (name, stream, i)
    f.write(str)
    f.close()

@app.route("/", methods=["POST"])
def new():
    r = request.json
    name = r["name"]
    streamsOut = r["streamsOut"]

    os.makedirs(name)
    for f in streamsOut:
        os.makedirs(os.path.join(name, f))
        playlistFile(name, f)

    return make_response("OK", 200)

@app.route("/<name>/<stream>/<filename>", methods=["POST"])
def retrieveStreamChunck(name, stream, filename):
    def download(request, stream, filename):
        path = os.path.join(name, stream, filename)
        ret = cm.file.download(request["id"])
        if ret[0] == 200:
            f = open(path, "wb")
            f.write(ret[1].getvalue())
            f.close()

    Thread(target=download, args=(request.json, stream, filename, )).start()
    return make_response("OK", 200)

@app.route("/<name>/<stream>", methods=["GET"])
def startStream(name, stream):
    def startEncode():
        folder = os.path.join(name, stream)
        plst = os.path.join(folder, "playlist.txt")
        outputfile = os.path.join(folder, "fullout.ts")
        address = "udp://" + targetPlayingAddress + "/" + name + "/" + stream
        print "start streaming to " + address
        cmd = ["ffmpeg", "-re", "-f", "concat", "-safe", "0", "-i", plst,
               "-b", "900k", "-f", "mpegts", outputfile]
        subprocess.call(cmd)

    def play():
        sleep(5)
        outputfile = os.path.join(name, stream, "fullout.ts")
        cmd = ["ffplay", "-i", outputfile]
        subprocess.call(cmd)

    Thread(target=startEncode).start()
    Thread(target=play).start()
    return make_response("OK", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, threaded=True)
