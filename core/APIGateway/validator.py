import re, json


def validateActionRequest(request):
    req = request.form.copy().to_dict()
    supportedLanguages = ("python")

    if not req:
        return (False, {"error": "Not a multipart-form"})
    try:
        if req['type'] != "action":
            return (False, {"error": "Wrong message type"})
        if req['name'] == "":
            return (False, {"error": "Action name needed"})
        if not req['language'].lower() in supportedLanguages:
            return (False, {"error": "Language supported are: " +
                    str(supportedLanguages)})
        if not req['cloud'].lower() in ("true", "false"):
            return (False, {"error": "Cloud must be a boolean"})
        req['in/out'] = json.loads(req['in/out'])
        if (type(req['in/out']['in']) != list or
           type(req['in/out']['out']) != list) :
            return (False, {"error": "the in/out field must contain the keys in \
                             and out with values lists"})
        req['description']
        int(req['timeout'])
        # TODO add other constraints
    except KeyError, e:
        return (False, {"error": "Field '" + str(e) + "' not present"})
    except ValueError, e:
        return (False, {"error": "Timeout must be an integer, in [ms]"})

    if 'file' not in request.files:
        return (False, {"error": "No file field!!!"})

    if request.files['file'].filename == '':
        return (False, {"error": "no file selected"})

    

    ret = {
        'name': req['name'],
        'description': req['description'],
        'language': req['language'],
        'cloud': req['cloud'] == 'true',
        'timeout': int(req['timeout']),
        'in/out': req['in/out'],
    }

    return (True, ret)

"""def cleanUpAct(req):
    fields = ("name", "description", "language", "cloud", "timeout")
    for k in req.keys():
        if k not in fields:
            del req[k]
    return req"""


def validateNodeRequest(request):
    req = request.json
        
    pattern = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}')
    supportedArch = ("arm")
    

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
            return (False, {"error": "Supported architecture are: " +
                    str(supportedArch)})
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
    fields = ("name", "ip", "architecture")
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
            return (False, {"error": "Sequence name needed"})
        if (type(req['in/out']['in']) != list or
           type(req['in/out']['out']) != list) :
            return (False, {"error": "the in/out field must contain the keys in \
                             and out with values lists"})
        req['process']
        req['description']
    except KeyError, e:
            return (False, {"error": "Field '" + str(e) + "' not present"})

    return (True, req)


def cleanUpSeq(req):
    fields = ("name", "description", "process", "in/out")
    for k in req.keys():
        if k not in fields:
            del req[k]
    return req

def validateInvoke(request):
    req = request.json
    actionClasses = {"small": 128,
                     "medium": 256,
                     "large": 512}
    if not req:
        return (False, {"error": "Not a JSON"})
    try:
        if type(req['param']) != dict:
            return (False, {"error": "'param' must contain a formatted json"})
        defClass = req['default']['actionClass']
        if (defClass not in actionClasses):
            return (False, {"error": "actionClass must be 'small', 'medium' or 'large'"})
    except KeyError, e:
            return (False, {"error": "Field '" + str(e) + "' not present"})
    req['default']['memory'] = actionClasses[defClass]

    try:
        for e in req["except"]:
            eClass = req["except"][e]['actionClass']
            if (eClass not in actionClasses):
                return (False, {"error": "actionClass must be 'small', 'medium' or 'large'"})
            req["except"][e]['memory'] = actionClasses[eClass]
    except KeyError, e:
        req["except"] = {}
    
    return (True, req)

def validateAWS(request):
    req = request.json

    pattern = re.compile("arn:(aws|aws-us-gov):iam::\d{12}:role/?[a-zA-Z_0-9+=,.@\-_/]+")

    if not req:
        return (False, {"error": "Not a JSON"})
    try:
        req["accessKeyID"]
        req["secretAccessID"]
        if not pattern.match(req["ARN"]):
            return (False, {"error": "ARN incorrect"})
    except KeyError, e:
            return (False, {"error": "Field '" + str(e) + "' not present"})

    return (True, req)