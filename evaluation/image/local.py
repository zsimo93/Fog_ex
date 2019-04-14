from pythonlib.connectionManager import ConnectionManager
import time
from threading import Thread

cm = ConnectionManager("192.168.5.10")
path = r'C:\Users\Simone\Desktop\tst\Star-Wars.png'

def init(awst=0):
    aws = str(awst)
    basep = "C:/Users/Simone/workspace_thesis/sample_actions/images"
    in_out = {"in": ["id1", "id2", "id3", "id4"], "out": ["retId"]}
    actionPath = basep + "/compose.py"
    r = cm.action.new("compose", "combine 4 images in one",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = basep + "/rotate.py"
    r = cm.action.new("rotate", "rotate 180 degr the image",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = basep + "/resize.py"
    r = cm.action.new("resize", "resize image to 200px",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = basep + "/blackWhite.py"
    r = cm.action.new("blackWhite", "image to black and white",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = basep + "/greyscale.py"
    r = cm.action.new("greyscale", "image to greyscale",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["id", "format"], "out": ["retId"]}
    sequence = [{"id": "1",
                 "name": "resize",
                 "map": {"id": "param/id", "formatOut": "param/format"}},
                {"id": "2",
                 "name": "blackWhite",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "3",
                 "name": "greyscale",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "4",
                 "name": "rotate",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "5",
                 "name": "compose",
                 "map": {"id1": "1/retId", "id2": "2/retId", "id3": "3/retId", "id4": "4/retId"}}]
    r = cm.sequence.new("imageProc", "transform an image in 4 ways and combine in one",
                        in_out, sequence)
    print r

def initPipe(awst=0):
    aws = str(awst)
    basep = "C:/Users/Simone/workspace_thesis/sample_actions/images/pipe"
    in_out = {"in": ["image1", "image2", "image3", "image4"], "out": ["image"]}
    actionPath = basep + "/compose.py"
    r = cm.action.new("compose_p", "combine 4 images in one",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["image", "formatOut"], "out": ["image"]}
    actionPath = basep + "/rotate.py"
    r = cm.action.new("rotate_p", "rotate 180 degr the image",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["image", "formatOut"], "out": ["image"]}
    actionPath = basep + "/resize.py"
    r = cm.action.new("resize_p", "resize image to 200px",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["image", "formatOut"], "out": ["image"]}
    actionPath = basep + "/blackWhite.py"
    r = cm.action.new("blackWhite_p", "image to black and white",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["image", "formatOut"], "out": ["image"]}
    actionPath = basep + "/greyscale.py"
    r = cm.action.new("greyscale_p", "image to greyscale",
                      "python", "imageProc", in_out, aws, 25, actionPath)
    print r

    in_out = {"in": ["image", "format"], "out": ["image"]}
    sequence = [{"id": "1",
                 "name": "resize_p",
                 "map": {"image": "param/image", "formatOut": "param/format"}},
                {"id": "2",
                 "name": "blackWhite_p",
                 "map": {"image": "1/image", "formatOut": "param/format"}},
                {"id": "3",
                 "name": "greyscale_p",
                 "map": {"image": "1/image", "formatOut": "param/format"}},
                {"id": "4",
                 "name": "rotate_p",
                 "map": {"image": "1/image", "formatOut": "param/format"}},
                {"id": "5",
                 "name": "compose_p",
                 "map": {"image1": "1/image", "image2": "2/image", "image3": "3/image", "image4": "4/image"}}]
    r = cm.sequence.new("imageProc_P", "transform an image in 4 ways and combine in one",
                        in_out, sequence)
    print r

def invoke(path=path, formatOut="PNG", optimise="True", n=""):
    import json
    begin = time.time()
    code, resp = cm.invoker.invoke("imageProc", {"id": "", "format": formatOut}, "small",
                                   log=True, filePath=path, paramID="id", optimise=optimise)
    jr = json.loads(resp)
    # log = jr["log"]
    del jr["log"]
    try:
        idOut = jr["retId"]
        code, buff, mime = cm.file.download(idOut)
        file = open(str(n) + "local-out." + formatOut, "wb")
        file.write(buff.read())
        file.close()
    except Exception:
        print jr
    elapsed = time.time() - begin
    """logfile = open(str(n) + "logfile.txt", "w")
    for line in log:
        logfile.write(line + "\n")
    logfile.close()"""
    print elapsed

def invokePipe(path, formatOut, optimise, n=""):
    import json
    begin = time.time()
    fin = open(path, "rb")
    data = fin.read().encode("base64")
    fin.close()
    code, resp = cm.invoker.invoke("imageProc_P", {"image": data, "format": formatOut}, "medium",
                                   log=False, optimise=optimise)
    r = json.loads(resp)
    try:
        vidOut = r["image"].decode("base64")
        file = open(str(n) + "local-out." + formatOut, "wb")
        file.write(vidOut)
        file.close()
    except:
        pass
    elapsed = time.time() - begin
    for line in r["log"]:
        print line
    print elapsed


def invokeTh(num, path=path, formatOut="PNG", optimise="True"):
    begin = time.time()
    ths = []
    for i in range(0, num):
        t = Thread(target=invoke, args=(path, formatOut, optimise, i,))
        t.start()
        ths.append(t)
    for t in ths:
        t.join()  # Wait for all threads to end
    elapsed = time.time() - begin
    print "Total time " + repr(elapsed)

def invokePipeTh(num, path, formatOut, optimise):
    begin = time.time()
    ths = []
    for i in range(0, num):
        t = Thread(target=invokePipe, args=(path, formatOut, optimise, i,))
        t.start()
        ths.append(t)
    for t in ths:
        t.join()  # Wait for all threads to end
    elapsed = time.time() - begin
    print "Total time " + repr(elapsed)


def remove(pipe):
    print cm.action.delete("compose" + pipe, force=True)
    print cm.action.delete("rotate" + pipe, force=True)
    print cm.action.delete("resize" + pipe, force=True)
    print cm.action.delete("blackWhite" + pipe, force=True)
    print cm.action.delete("greyscale" + pipe, force=True)
