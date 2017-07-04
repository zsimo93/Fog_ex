from flask import make_response
from actionmanager import ActionManager
# from blockmanager import BlockManager
from core.utils.fileutils import deleteActionFiles
import traceback, os

def invoke(request):
    req = request.json

    # current node ARM or x86?
    try:
        if(req['type'] == "action"):
            action = req['action']
            map = req['map']
            seqID = req["seqID"]
            myID = req["myID"]
            r = ActionManager(action, seqID, myID, map).initAndRun()
            """else:
                r = BlockManager(req['block'], req['param']).run()"""

        return make_response(r)
    except Exception:
        tb = traceback.format_exc()
        return make_response(tb, 500)

def delFiles(token):
    deleteActionFiles()
    return make_response("OK", 200)

def setup(request):
    req = request.json

    os.environ['TH_ROLE'] = req['role']
    os.environ['TH_NAME'] = req['name']

    return make_response("OK", 200)