from ffmpy import FFmpeg
import io
from fileModule import FileManager
from subprocess import PIPE, call

call(["chmod", "+x", "ffmpeg"])

def main(args):
    inId = args["videoID"]
    inconf = ""
    outconf = "-f mpegts -vf scale=320:-1"

    fm = FileManager()
    data = fm.loadFile(inId)
    datared = data.read()

    ff = FFmpeg(
        inputs={"pipe:0": inconf},
        outputs={"pipe:1": outconf})

    o1, o2 = ff.run(input_data=datared, stdout=PIPE)

    bs = io.BytesIO(o1)
    outId = fm.saveFile(bs, "res-" + data.filename)

    return {"videoID": outId}
