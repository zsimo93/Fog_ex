from core.databaseMongo import actionsDB as adb, sequencesDB as sdb
from flask import make_response, jsonify
from core.handlers.execHandler import giveMeHandler
from validator import validateInvoke
from core.utils.fileutils import uniqueName
import json

def checkAvailableAndParam(token, param):
    if adb.availableActionName(token) and sdb.availableSeqName(token):
        # action name not present
        return False, "No action with name '" + token + "'"
    
    ok, wrong = sdb.checkInputParam(token, param.keys())
    if not ok:
        # a parameter needed by the action is not in the param dictionary
        return False, "'" + wrong + "' field needed but not in param."

    return True, None

def invoke(token, request):
    ok, resp = validateInvoke(request)
    if not ok:
        return make_response(jsonify(resp), 406)

    r = resp
    param = r["param"]
    ok, errmsg = checkAvailableAndParam(token, param)
    if not ok:
        return make_response(jsonify({'error': errmsg}), 406)
    
    sessionID = uniqueName()
    hand = giveMeHandler(r["param"], r["default"], r["except"],
                         token, sessionID)
    payload, code = hand.start()
    try:
        result = json.loads(payload)
    except Exception:
        result = payload

    try:
        if resp["log"]:
            result["log"] = hand.logList
    except KeyError:
        pass

    return make_response(jsonify(result), code)
