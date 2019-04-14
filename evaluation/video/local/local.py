from pythonlib.connectionManager import ConnectionManager
import time

cm = ConnectionManager("192.168.5.10")
path = r'C:\Users\Simone\Desktop\tst\output000.ts'
def init():
    in_out = {"in": ["videoID", "inConf", "outConf", "namePrefix"], "out": ["outID"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/videos/genericFFmpeg.py"
    r = cm.action.new("videoEdit", "generic ffmpeg editor",
                      "python", "ffmpeg", in_out, "0", 25, actionPath)
    print r

    in_out = {"in": ["videoId", "inConf1", "outConf1", "inConf2", "outConf2", "namePrefix"],
              "out": ["outID"]}
    sequence = [{"id": "1",
                 "name": "videoEdit",
                 "map": {"videoID": "param/videoId",
                         "inConf": "param/inConf1",
                         "outConf": "param/outConf1",
                         "namePrefix": "param/namePrefix"}},
                {"id": "2",
                 "name": "videoEdit",
                 "map": {"videoID": "1/outID",
                         "inConf": "param/inConf2",
                         "outConf": "param/outConf2",
                         "namePrefix": "param/namePrefix"}}]
    r = cm.sequence.new("streamProcess", "resize and greyscale video",
                        in_out, sequence)
    print r

def initPipe():
    in_out = {"in": ["video", "inConf", "outConf", "namePrefix"], "out": ["video"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/videos/genericFFmpeg_p.py"
    r = cm.action.new("videoEdit_p", "generic ffmpeg editor",
                      "python", "ffmpeg", in_out, "0", 25, actionPath)
    print r

    in_out = {"in": ["video", "inConf1", "outConf1", "inConf2", "outConf2", "namePrefix"],
              "out": ["video"]}
    sequence = [{"id": "1",
                 "name": "videoEdit_p",
                 "map": {"video": "param/video",
                         "inConf": "param/inConf1",
                         "outConf": "param/outConf1",
                         "namePrefix": "param/namePrefix"}},
                {"id": "2",
                 "name": "videoEdit_p",
                 "map": {"video": "1/video",
                         "inConf": "param/inConf2",
                         "outConf": "param/outConf2",
                         "namePrefix": "param/namePrefix"}}]
    r = cm.sequence.new("streamProcess_p", "resize and greyscale video",
                        in_out, sequence)
    print r

def invoke(path, opt):
    import json
    begin = time.time()
    param = {
        "videoId": "",
        "inConf1": "-hide_banner -loglevel panic",
        "outConf1": "-f mpegts -vf scale=320:-1 ",
        "inConf2": "-hide_banner -loglevel panic -f mpegts",
        "outConf2": "-f mpegts -vf hue=s=0 ",
        "namePrefix": ""}
    code, resp = cm.invoker.invoke("streamProcess", param, "medium",
                                   log=True, filePath=path, paramID="videoId", optimise=opt)
    jr = json.loads(resp)
    idOut = jr["outID"]
    code, buff, mime = cm.file.download(idOut)
    file = open("local-out.ts", "wb")
    file.write(buff.read())
    file.close()
    elapsed = time.time() - begin
    logfile = open("log.txt", "w")
    for line in jr["log"]:
        logfile.write(line + "\n")
    logfile.close()
    print elapsed
    return elapsed

def invokePipe(path, opt):
    import json
    begin = time.time()
    fin = open(path, "rb")
    data = fin.read().encode("base64")
    fin.close()
    param = {
        "video": data,
        "inConf1": "-hide_banner -loglevel panic",
        "outConf1": "-f mpegts -vf scale=320:-1 ",
        "inConf2": "-hide_banner -loglevel panic -f mpegts",
        "outConf2": "-f mpegts -vf hue=s=0 ",
        "namePrefix": ""}
    code, resp = cm.invoker.invoke("streamProcess_p", param, "medium",
                                   log=True, optimise=opt)
    #print resp
    r = json.loads(resp)
    idOut = r["video"].decode("base64")
    file = open("local-out.ts", "wb")
    file.write(idOut)
    file.close()
    elapsed = time.time() - begin

    logfile = open("log.txt", "w")
    for line in r["log"]:
        logfile.write(line + "\n")
    logfile.close()
    print elapsed


def run():
    one = open("one-no", "w")

    for i in range(0, 20):
        num = invokePipe(path, "False")
        one.write(repr(num) + "\n")
        time.sleep(1)

    one.close()

    one = open("one-opt", "w")

    for i in range(0, 20):
        num = invokePipe(path, "True")
        one.write(repr(num) + "\n")
        time.sleep(1)

    one.close()
