#!thesis/api
from flask import make_response, jsonify
from core.databaseMongo import (actionsDB as db,
                                sequencesDB as sdb,
                                tokenDB as tdb,
                                dependenciesDB as depdb,
                                awsCredential as aws)
from core.databaseMongo.nodesDB import getNodesIP
from core.gridFS import files as fs
from core.utils.httpUtils import post
from validator import validateActionRequest as validate
from requests import ConnectionError
from core.aws.lambdaconnector import AwsActionCreator, AwsActionDeletor
"""
def computeAvailability(name, request):
    nList = [n["_id"] for n in getNodes()]

    db.updateAvailability(name, nList)
"""

def newAction(request):
    valid, resp = validate(request)

    file = request.files['file']

    if not valid:
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")

    if not db.availableActionName(name) or not sdb.availableSeqName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)

    if resp["cloud"] == "2" and not aws.checkPresence():
        return make_response(jsonify({'error': "Forced execution on cloud but no AWS credentials"}), 406)

    if resp["cloud"] == "0":
        pass
    else:  # cloud 1 or 2
        if not aws.checkPresence():
            resp["cloud"] = "0"

        else:
            ac = AwsActionCreator(name, resp["language"],
                                  resp["description"], resp["timeout"],
                                  file, resp["contTag"])
            ac.create()

    fs.saveActionFile(file, name)

    db.insertAction(name, resp)

    # computeAvailability(name, resp)

    return make_response(name, 201)


def actualdelete(actionname):
    deleted = db.deleteAction(actionname)
    tdb.deleteToken(actionname)
    fs.removeActionFile(actionname)
    if deleted["cloud"]:
        try:
            AwsActionDeletor(actionname).delete()
        except Exception:
            pass
    try:
        payload = {"containerName": deleted["containerName"]}
    except KeyError:
        payload = {}

    for n in getNodesIP():
        try:
            post(str(n.ip), 8080, "/internal/delete/" + str(actionname), payload)
        except ConnectionError:
            pass


def deleteAction(request, actionname):

    if db.availableActionName(actionname):   # action name not present
        return make_response(jsonify({'error': "No action with name " + actionname}),
                             406)

    deplist = depdb.getDependencies(actionname)
    if not deplist:
        actualdelete(actionname)
        return make_response("OK", 200)

    try:
        token = str(request.json['token'])
        if tdb.checkToken(actionname, token):
            actualdelete(actionname)
            return make_response("OK", 200)
    except Exception:
        pass

    newtoken = tdb.newToken(actionname)
    resp = {"message": "By deleting this action also the actions in the list will be deleted. Resend the request with the token to confirm.",
            "dependencies": deplist,
            "token": newtoken}
    return make_response(jsonify(resp), 202)


def getActions(request):
    actions = db.getActions()
    return make_response(jsonify({"actions": actions}), 200)
