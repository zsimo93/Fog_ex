#!thesis/api
from flask import make_response, jsonify
from core.databaseMongo import nodesDB as db, mainDB
from validator import validateNodeRequest as validate, cleanUpNode as clean
from pymongo.errors import OperationFailure
"""
def computeAvailability(resp, nodeId):
    alist = [n["_id"] for n in actionsDB.getActions()]

    for actionId in alist:
        actionsDB.updateAvailability(actionId, nodeId)
"""

def newNode(request):
    
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)
    if db.getNode(resp["name"]):
        error = {"error": "Name '" + resp["name"] + "' already in use"}
        return make_response(jsonify(error), 400)
    """
    if resp.pop('setup'):
        user = resp.pop("ssh_user")
        password = resp.pop("ssh_password")
    """
    # TODO RUN SETUP

    resp = clean(resp)  # remove unwanted fields before storing in DB
    try:
        id = db.insertNode(resp)
    except OperationFailure as e:
        print e
        return make_response(jsonify({"error": "First run the mongoDB instance on the target node"}), 400)
    # computeAvailability(resp, id)
    
    return make_response(id, 200)


def deleteNode(request, token):
    
    if not db.getNode(token):
        return make_response(jsonify({'error': "No node with id " + token}),
                             406)

    msg = db.deleteNode(token)
    
    return make_response(msg, 200)


def getNodes(request):
    nodes = db.getNodes()
    return make_response(jsonify({"nodes": nodes}), 200)

def reset(request):
    mainDB.resetReplicaSet()
    return make_response("OK", 200)
