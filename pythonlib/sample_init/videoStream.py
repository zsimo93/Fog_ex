from pythonlib.connectionManager import ConnectionManager

def init():
    cm = ConnectionManager("192.168.1.50")

    in_out = {"in": ["videoID", "inConf", "outConf", "namePrefix"], "out": ["outID"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/videos/genericFFmpeg.py"
    r = cm.action.new("videoEdit", "generic ffmpeg editor",
                      "python", "ffmpeg", in_out, "0", 25, actionPath)
    print r

    in_out = {"in": ["videoId", "inConf", "outConf", "namePrefix"], "out": {"bw": "1/outID", "original": "param/videoId"}}
    sequence = [{"id": "1",
                 "name": "videoEdit",
                 "map": {"videoID": "param/videoId",
                         "inConf": "param/inConf",
                         "outConf": "param/outConf",
                         "namePrefix": "param/namePrefix"}}]
    r = cm.sequence.new("streamProcess", "output id of video in black&white and original",
                        in_out, sequence)
    print r
