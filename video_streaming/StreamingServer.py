from flask import Flask, make_response, request
import os
from ..pythonlib import connectionManager
import subprocess
from threading import Thread

app = Flask(__name__)
cm = connectionManager.ConnectionManager("192.168.1.50")
targetPlayingAddress = "192.168.1.4:1234"

def playlistFile(name, stream):
    path = os.path.join(name, stream, "playlist.txt")
    f = open(path, "w+")

    str = ""
    for i in range(0, 400):
        str += "file '.\\%s\\%s\\output%03d.avi'\n" % (name, stream, i)
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
    def startThread(request, stream, filename):
        path = os.path.join(name, stream, filename)
        ret = cm.file.download(request["id"])
        if ret[0] == 200:
            f = open(path, "wb")
            f.write(ret[1].getvalue())
            f.close()

    Thread(target=startThread, args=(request.json, stream, filename, )).start()
    return make_response("OK", 200)

@app.route("/<name>/<stream>", methods=["GET"])
def startStream(name, stream):
    def startThread():
        plst = os.path.join(name, stream, "playlist.txt")
        address = "udp://" + targetPlayingAddress + "/" + name + "/" + stream
        print "start streaming to " + address
        # cmd = ["ffmpeg", "-re", "-f", "concat", "-i", plst, "-vcodec", "libx264",
        #       "-tune", "zerolatency", "-b", "900k", "-f", "mpegts", address]
        cmd = ["ffplay", "-f", "concat", "-i", plst]
        subprocess.call(cmd)

    Thread(target=startThread).start()
    return make_response("OK", 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222, threaded=True)
