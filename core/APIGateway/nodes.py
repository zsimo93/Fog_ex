#!thesis/api

from flask import make_response, jsonify
from core.databaseMongo import nodesDB as db
from validator import validateNodeRequest as validate, cleanUpNode as clean

def newNode(request):
    
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    if resp.pop('setup'):
        user = resp.pop("ssh_user")
        password = resp.pop("ssh_password")

        # TODO RUN SETUP

    resp = clean(resp)  # remove unwanted fields before storing in DB
    
    # TODO compute actions to add and update availability

    id = db.insertNode(resp)

    return make_response(id, 200)


def deleteNode(request, token):
    
    if not db.getNode(token):
        return make_response(jsonify({'error': "No node with id " + token}),
                             406)

    db.deleteNode(token)
    
    return make_response("OK", 200)


def getNodes(request):
    nodes = db.getNodes()
    return make_response(jsonify({"nodes": nodes}), 200)
