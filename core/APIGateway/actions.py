#!thesis/api

from core.databaseMongo import actionsDB as db
from core.gridFS import fileUtils as fs
from validator import validateActionRequest as validate
from core.utils.httpUtils import post


def newAction(request):
    valid, resp = validate(request)

    if 'file' not in request.files:
        return make_response("file!!!", 400)

    file = request.files['file']
    
    if not valid:
        print(resp)
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")

    if not db.availableActionName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)
    
    fs.saveFile(file, name)

    db.insertAction(name, resp)

    # TODO compute where to deploy action and update availability

    return make_response(name, 201)


"""
def downloadAction(token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name " + token}),
                             406)

    (path, type) = fs.loadFile(token)
    return send_file(path, mimetype=type)
"""
def updateAction(request, token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name " + token}),
                             406)

    # TODO
    return make_response("NOT IMPL", 200)


def deleteAction(request, token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name " + token}),
                             406)

    db.deleteAction(token)
    fs.removeFile(token)
    return make_response("OK", 200)


def invokeAction(request, token):
    if db.availableActionName(token):  # action name not present
        return make_response(jsonify({'error': "No action with name " + token}),
                             406)
    
    param = request.json["message"]

    # TODO placement, invocation...

    ip = selectBestNode(token)

    ret = post(ip, "8080", "/internal/invoke", param)

    return make_response(ret, 200)


def getActions(request):
    actions = db.getActions()
    return make_response(jsonify({"actions": actions}), 200)