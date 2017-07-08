from core.databaseMongo import actionsDB as adb, sequencesDB as sdb
from flask import make_response, jsonify
from handlers import giveMeHandler
from validator import validateInvoke
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
    
    hand = giveMeHandler(r["param"], r["default"], r["except"], token)
    payload, code = hand.start()
    try:
        return make_response(jsonify(json.loads(payload)), code)
    except Exception:
        return make_response(jsonify(payload), code)