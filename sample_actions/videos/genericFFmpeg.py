from ffmpy import FFmpeg
import io
from fileModule import FileManager
from subprocess import PIPE

def main(args):

    inId = args["videoID"]
    inconf = None if not args["inConf"] else args["inConf"]
    outconf = None if not args["outConf"] else args["outConf"]
    prefix = args["namePrefix"]
    
    fm = FileManager()
    data = fm.loadFile(inId)
    datared = data.read()
    
    """
    conf = '-v error -of flat=s=_ -select_streams v:0 \
    -show_entries stream=codec_name,height,width,pix_fmt,r_frame_rate -of default=noprint_wrappers=1:nokey=1 \
    -show_entries format=format_name -of default=noprint_wrappers=1:nokey=1'

    fp = FFprobe(
        inputs={"pipe:0": conf})


    stdout, stderr = fp.run(input_data=datared, stdout=PIPE)
    print stdout
    l = stdout.split("\n")
    hxw = l[1] + "x" + l[2]
    codec = l[0]
    pix_fmt = l[3]
    rate = l[4]
    format = "webm"
    """

    ff = FFmpeg(
        inputs={"pipe:0": inconf},
        outputs={"pipe:1": outconf})

    o1, o2 = ff.run(input_data=datared, stdout=PIPE)

    bs = io.BytesIO(o1)
    outId = fm.saveFile(bs, prefix + data.filename)

    return {"outID": outId}
