import sys
from pythonlib import ConnectionManager
import pyinotify
import json
import requests
import os
from threading import Thread

def main():
    name = sys.argv[1]
    streamingServerIP = "http://192.168.1.8:2222/"
    streamsOut = sys.argv[2:]

    def createFolders():
        post = {
            "name": name,
            "streamsOut": streamsOut
        }
        requests.post(streamingServerIP, json=post)
    #######################

    def streamVideo(path):
        sys.stdout.write(
            'video complete: {}\n'.format(path)
        )
        sys.stdout.flush()
        cm = ConnectionManager("192.168.1.50")
        param = {
            "videoId": "",
            "inConf": "",
            "outConf": "-f mpegts -vf hue=s=0 ",
            "namePrefix": ""}
        res = cm.invoker.invoke("streamProcess", param, "small",
                                {"streamProcess": {"actionClass": "large"}}, filePath=path, paramID="videoId")
        if res[0] != 200:
            res = cm.invoker.invoke("streamProcess", param, "small",
                                    {"streamProcess": {"actionClass": "large"}}, filePath=path, paramID="videoId")
        print res
        idsOut = json.loads(res[1])["fileIds"]
        filename = os.path.basename(path)

        for stream in idsOut:
            addr = streamingServerIP + name + "/" + stream + "/" + filename
            requests.post(addr, json={"id": idsOut[stream]})

            if filename.split(".")[0].endswith("002"):
                addr = streamingServerIP + name + "/" + stream
                requests.get(addr)

    class VideoComplete(pyinotify.ProcessEvent):
        def process_IN_MOVED_TO(self, event):
            Thread(target=streamVideo, args=(event.pathname,)).start()

        def process_IN_CLOSE_WRITE(self, event):
            Thread(target=streamVideo, args=(event.pathname,)).start()

    createFolders()
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, VideoComplete())

    mask = pyinotify.ALL_EVENTS
    path = './files'
    wm.add_watch(path, mask, rec=True, auto_add=True)
    notifier.loop()


if __name__ == '__main__':
    main()
