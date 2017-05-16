#!thesis/api

from flask import make_response, jsonify
from core.databaseRedis import nodeUtils as utils
from validator import validateNodeRequest as validate
from core.utils import uniqueName

def newNode(request):
    
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    id = uniqueName()
    resp['id'] = id
    resp['mqtt_Topic'] = "node/" + id
    
    if resp.pop('setup'):
        user = resp.pop("ssh_user")
        password = resp.pop ("ssh_password")

        #TODO RUN SETUP

    utils.insertNode(resp)

    return make_response(id, 200)


def deleteNode(request, token):
    
    if not utils.getNode(token):
        return make_response(jsonify({'error': "No node with id " + token}), 406)

    utils.deleteNode(token)
    
    return make_response("OK", 200)


def getNodes(request):
    nodes = utils.getNodes()
    return make_response(jsonify({"nodes": nodes}), 200)
