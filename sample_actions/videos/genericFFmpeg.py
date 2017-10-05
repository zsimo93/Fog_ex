from ffmpy import FFmpeg
import io, time
from fileModule import FileManager
from subprocess import PIPE

def main(args):

    inId = args["videoID"]
    inconf = None if not args["inConf"] else args["inConf"]
    outconf = None if not args["outConf"] else args["outConf"]
    prefix = args["namePrefix"]

    fm = FileManager()
    begin = time.time()
    data = fm.loadFile(inId)
    elapsed = time.time() - begin
    print ("read Time " + repr(elapsed))
    datared = data.read()

    ff = FFmpeg(
        inputs={"pipe:0": inconf},
        outputs={"pipe:1": outconf})

    o1, o2 = ff.run(input_data=datared, stdout=PIPE)

    bs = io.BytesIO(o1)
    begin = time.time()
    outId = fm.saveFile(bs, prefix + data.filename)
    elapsed = time.time() - begin
    print ("write Time " + repr(elapsed))
    return {"outID": outId}
