import json
import re


def validateActionRequest(request):
    req = request.json

    supportedLanguages = ("python", "java")
    
    if not req:
        return (False, {"error": "Not a JSON"})
    try:
        if req.pop('type') != "function":
            return (False, {"error": "Wrong message type"})
        if req['name'] == "":
            return (False, {"error": "Action name needed"})
        if not req['language'].lower() in supportedLanguages:
            return (False, {"error": "Language supported are: " + str(supportedLanguages)})
        if not type(req['cloud']) == bool:
            return (False, {"error": "Cloud must be a boolean"})
        if not type(req['timeout']) == int:
            return (False, {"error": "Timeout must be an integer"})
        req['description']
        # TODO add other constraints
    except KeyError, e:
        return (False, {"error": "Field '" + str(e) + "' not present"})

    return (True, req)

def cleanUpAct(req):
    fields = ("type", "name", "description", "language", "cloud", "timeout")
    for k in req.keys():
        if k not in fields:
            del req[k]
    return req


def validateNodeRequest(request):
    req = request.json
        
    pattern = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')
    supportedArch = ("arm", "x86")
    

    if not req:
        return (False, {"error": "Not a JSON"})
    try:
        if req.pop('type') != "node":
            return (False, {"error": "Wrong message type"})
        if req['name'] == "":
            return (False, {"error": "Function name needed"})
        if not pattern.match(req['ip']):
            return (False, {"error": "Invalid IP"})
        if not req['architecture'].lower() in supportedArch:
            return (False, {"error": "Supported architecture are: " + str(supportedArch)})
        if not type(req['setup']) == bool:
            return (False, {"error": "Setup must be a boolean"})
    except KeyError, e:
        return (False, {"error": "Field '" + str(e) + "' not present"})

    if req['setup']:
        try:
            req['ssh_user']
            req['ssh_password']
        except KeyError, e:
            return (False, {"error": "Field '" + str(e) + "' not present"})

    return (True, req)


def cleanUpNode(req):
    fields = ("type", "name", "ip", "architecture")
    for k in req.keys():
        if k not in fields:
            del req[k]
    return req


def validateSequence(request):
    req = request.json

    if not req:
        return (False, {"error": "Not a JSON"})
    try:
        if req.pop('type') != "sequence":
            return (False, {"error": "Wrong message type"})
        if req['name'] == "":
            return (False, {"error": "Function name needed"})
        if not type(req['sequence']) == list:
            return (False, {"error": "Sequence must be a list of lists"})
        req['description']
    except KeyError, e:
            return (False, {"error": "Field '" + str(e) + "' not present"})

    return (True, req)


def cleanUpSeq(req):
    fields = ("type", "name", "description", "sequence")
    for k in req.keys():
        if k not in fields:
            del req[k]
    return req