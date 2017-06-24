from flask import make_response
from actionmanager import ActionManager
# from blockmanager import BlockManager
from core.utils.fileutils import deleteActionFiles

"""
__action__ = {
    "name": "",
    "cpu": 0,
    "memory": 0,
}

request.json = {
    "type": "action",
    "param": {},
    "action": __action__
}

request.json = {
    "type": "block",
    "param": {}
    "block": [
        __action__,
        __action__
    ]
}
"""

def invoke(request):
    req = request.json

    # current node ARM or x86?
    try:
        if(req['type'] == "action"):
            action = req['action']
            param = req['param']
            seqID = req["seqID"]
            myID = req["myID"]
            r = ActionManager(action, seqID, myID, param).initAndRun()
        """else:
                        r = BlockManager(req['block'], req['param']).run()"""

        return make_response(r)
    except Exception, e:
        return make_response(str(e), 500)

def delFiles(token):
    deleteActionFiles()
    pass