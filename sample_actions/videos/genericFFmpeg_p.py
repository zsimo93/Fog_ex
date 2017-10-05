from ffmpy import FFmpeg
from subprocess import PIPE

def main(args):
    invid = args["video"].decode("base64")
    inconf = None if not args["inConf"] else args["inConf"]
    outconf = None if not args["outConf"] else args["outConf"]

    ff = FFmpeg(
        inputs={"pipe:0": inconf},
        outputs={"pipe:1": outconf})

    o1, o2 = ff.run(input_data=invid, stdout=PIPE)

    return {"video": o1.encode("base64")}
