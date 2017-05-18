#!thesis/api

from flask import make_response, jsonify, send_file
from core.databaseRedis import actionsDB as db
from validator import validateActionRequest as validate, cleanUpAct as clean
from core.utils import saveAction 


def newAction(request):
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp, 400))

    name = resp.pop("name")

    if not db.availableActionName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)
    
    resp = clean(resp)  # remove unwanted fields before storing in DB
    db.insertAction(name, resp)
    return make_response(name, 201)


def uploadAction(request, token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    # replication in other nodes
    
    data = request.files['file']
    saveAction(token, data)

    return make_response("OK", 200)

def downloadAction(token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    return send_file("/path/to/file/" + token)

def updateAction(request, token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    # TODO
    return make_response("NOT IMPL", 200)


def deleteAction(request, token):
    if db.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    db.delActionDB(token)
    # TODO remove files from all nodes
    return make_response("OK", 200)


def invokeAction(request, token):
    if db.availableActionName(token):  # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)
    
    # TODO placement, invocation...
    return make_response("NOT IMPL", 200)


def getActions(request):
    actions = db.getActions()
    return make_response(jsonify({"actions": actions}), 200)