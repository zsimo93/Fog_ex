import re, json


def validateActionRequest(request):
    req = request.form.copy().to_dict()
    supportedLanguages = ("python", "java")

    print req
    
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
        'in/out': req['in/out']
    }

    print ret

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
    print req
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