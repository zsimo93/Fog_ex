from core.databaseMongo import actionsDB as adb, sequencesDB as sdb
from executionmanager import ExecutionManager
from flask import make_response, jsonify

def checkAvailableAndParam(token, param):
    if adb.availableActionName(token) and sdb.availableSeqName(token):
        # action name not present
        return False, "No action with name '" + token + "'"
    
    ok, wrong = sdb.checkInFields(token, param.keys())
    if not ok:
        # a parameter needed by the action is not in the param dictionary
        return False, "'" + wrong + "' field needed but not in param."

    return True, None

def invoke(token, request):
    param = request.json["param"]
    ok, errmsg = checkAvailableAndParam(token, param)
    if not ok:
        return make_response(jsonify({'error': errmsg}), 406)
    
    ret = function_To_Start(token, request.json)
    return make_response(ret)


