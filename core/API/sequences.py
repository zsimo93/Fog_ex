#!thesis/api

from flask import make_response, jsonify
from validator import validateSequence as validate
from core.databaseRedis import sequenceUtils as utils

def newSequence(request):

    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")
    
    if not utils.availableSeqName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)

    # check all functions in list are available
    l = resp['sequence']
    a = utils.checkSequence(l)
    if a:
        return make_response(jsonify({"error": "Action " + a + " not present"}), 400)
    
    utils.insertSequence(name, resp)
    return make_response(name, 201)


def deleteSequence(request, token):
    
    if not utils.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    utils.deleteSequence(token)
    return make_response("OK", 200)


def invokeSequence(request, token):
    
    if not utils.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    # TODO placement, invocation...
    pass

def getSequences(request):
    seq = utils.getSequences()
    return make_response(jsonify({"sequences": seq}), 200)