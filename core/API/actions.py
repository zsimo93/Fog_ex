#!thesis/api

from flask import make_response, jsonify
from core.databaseRedis import actionUtils as utils
from validator import validateActionRequest as validate
import os

def newAction(request):
    
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp, 400))

    name = resp.pop("name")

    if not utils.availableActionName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)
    
    utils.insertAction(name, resp)
    return make_response(name, 201)


def updateAction(request, token):
    
    if utils.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    # TODO
    return make_response("NOT IMPL", 200)


def deleteAction(request, token):
    
    if utils.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    utils.delActionDB(token)
    # TODO remove files from all nodes
    return make_response("OK", 200)



def uploadAction(request, token):

    if utils.availableActionName(token):   # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)

    # TODO Move somewhere else?, replication in other nodes
    path = ("/home/pi")
    new_path = path + str(token)

    try:
        os.stat(new_path)
    except:
        os.mkdir(new_path)

    data = request.files['file']
    path = os.path.join(new_path, data.filename)

    print data.save(path)

    return make_response("OK", 200)


def invokeAction(request, token):

    if utils.availableActionName(token):  # action name not present
        return make_response(jsonify({'error': "No action with name" + token}), 406)
    
    # TODO placement, invocation...
    return make_response("NOT IMPL", 200)


def getActions(request):
    actions = utils.getActions()
    return make_response(jsonify({"actions": actions}), 200)