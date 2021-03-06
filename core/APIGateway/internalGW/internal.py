from flask import make_response
from actionmanager import ActionManager
from blockmanager import BlockManager
from core.container.dockerInterface import delImage
from core.utils.fileutils import deleteActionFiles
import traceback, os
import threading
from core.container.dockerInterface import pullImage
from core.databaseMongo import localDB

def invoke(request):
    req = request.json

    # current node ARM or x86?
    try:
        if(req['type'] == "action"):
            action = req['action']
            sessionID = req["sessionID"]
            inparam = req["param"]
            nlog = req["needlog"]
            r = ActionManager(action, nlog, inparam, sessionID).initAndRun()
        else:
            block = req['block']
            sessionID = req["sessionID"]
            inparam = req["param"]
            nlog = req["needlog"]
            r = BlockManager(block, nlog, inparam, sessionID).run()

        return make_response(r)
    except Exception:
        tb = traceback.format_exc()
        return make_response(tb, 500)

def delFiles(token, request):
    localDB.deleteActionContainers(token)
    deleteActionFiles(token)
    try:
        contName = request.json["containerName"]
        delImage(contName)
    except Exception:
        pass

    return make_response("OK", 200)

def downloadImage(request):
    contname = request.json["contName"]
    threading.Thread(target=pullImage, args=(contname,))
    return make_response("OK", 200)

def setup(request):
    req = request.json

    os.environ['TH_NAME'] = req['name']

    return make_response("OK", 200)
