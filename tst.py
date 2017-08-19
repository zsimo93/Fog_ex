from ffmpy import FFmpeg
import io
ff = FFmpeg(
    inputs={'pipe:0': '-vcodec libx264'},
    outputs={'final.avi': None})

print ff.cmd

file = open("small.mp4", "rb")
buff = io.BytesIO
ff.run(input_data=file.read())