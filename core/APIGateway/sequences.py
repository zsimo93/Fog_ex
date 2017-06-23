#!thesis/api
from flask import Flask, request, make_response, jsonify
from validator import validateSequence as validate, cleanUpSeq as clean
from core.databaseMongo import sequencesDB as db
from executionmanager import SeqExecutionManager

def newSequence(request):
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")
    
    if not db.availableSeqName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)

    # check availability of functions in the list and matching of in/out param
    l = resp['process']
    ok, errorMsg = db.checkSequence(l, resp["in/out"])
    if not ok:
        return make_response(jsonify({"error" : errorMsg}), 400)
    resp = clean(resp)  # remove unwanted fields before storing in DB
    db.insertSequence(name, resp)
    return make_response(name, 201)


def deleteSequence(request, token):
    
    if db.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    db.deleteSequence(token)
    return make_response("OK", 200)


def invokeSequence(request, token):
    
    if db.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    man = SeqExecutionManager(request.json, token)
    ret = man.run()

    return make_response(ret)


def getSequences(request):
    seq = db.getSequences()
    return make_response(jsonify({"sequences": seq}), 200)