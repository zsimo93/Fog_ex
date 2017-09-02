import collections
import cv
import os


__FRAMES_PER_SECOND = 10.0

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def play(file):
    vidFile = cv.CaptureFromFile(file)
    nFrames = int(cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FRAME_COUNT))
    fps = cv.GetCaptureProperty(vidFile, cv.CV_CAP_PROP_FPS)
    waitPerFrameInMillisec = int(1 / __FRAMES_PER_SECOND * 1000 / 1)
    for f in xrange( nFrames ):
      frameImg = cv.QueryFrame( vidFile )
      cv.ShowImage( "My Video Window",  frameImg )
      cv.WaitKey( waitPerFrameInMillisec  )



directory = "vids/"
dictFiles = {}
arrFiles = []
for root, dirs, files in os.walk(directory):
    #print root
    #print dirs
    arrFiles = files
for file in arrFiles:
    number = find_between(file, "[", "]")
    #print "----------",file
    dictFiles[number] = file

orderedDictFiles = collections.OrderedDict(sorted(dictFiles.items()))
for file in orderedDictFiles:
    play(directory + orderedDictFiles[file])
