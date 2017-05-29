from flask import make_response
from threading import Thread
from actionmanager import ActionManager
from blockmanager import BlockManager

"""
__action__ = {
    "name": "",
    "cpu": 0,
    "memory": 0,
    "param": {}
}

request.json = {
    "type": "action",
    "data": __action__
}

request.json = {
    "type": "block",
    "data": {
        "param": {},
        "block": [
            __action__,
            __action__
        ]
    }
}
"""

def invoke(request):
    req = request.json

    # current node ARM or x86?

    if(req['type'] == "action"):
        action = req['data']
        param = action.pop('param')
        r = ActionManager(action, param=param).initAndRun()
    else:
        r = BlockManager(req['data']).run()

    return make_response(r)



def fetch(token):
    pass