#!thesis/api
from flask import make_response, jsonify
from validator import validateSequence as validate, cleanUpSeq as clean
from core.databaseMongo import (sequencesDB as db,
                                actionsDB as adb,
                                tokenDB as tdb,
                                dependenciesDB as depdb)

from core.handlers.flatsequence import unrollAndDAG
from core.handlers.seqanalizer import SequenceAnalizer

def newSequence(request):
    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")
    
    if not db.availableSeqName(name) or not adb.availableActionName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)

    # check availability of functions in the list and matching of in/out param
    proc = resp['sequence']
    ok, errorMsg = db.checkSequence(proc, resp["in/out"])
    if not ok:
        return make_response(jsonify({"error" : errorMsg}), 400)
    
    resp = clean(resp)  # remove unwanted fields before storing in DB
    resp["fullSeq"] = unrollAndDAG(proc)
    resp["execSeq"] = SequenceAnalizer(resp["fullSeq"]).__json__()
    resp["resultActionID"] = resp["fullSeq"][-1]["id"]
    db.insertSequence(name, resp)  # save seq in db
    depdb.computeDep(name, proc)  # save all the dependencies usefull for delete
    return make_response(name, 201)


def deleteSequence(request, actionname):
    
    def actualdelete():
        db.deleteSequence(actionname)
        tdb.deleteToken(actionname)
        return make_response("OK", 200)
    
    if db.availableSeqName(actionname):
        return make_response(jsonify({'error': "No sequence with name" + actionname}), 406)

    deplist = depdb.getDependencies(actionname)
    if not deplist:
        return actualdelete()
        
    try:
        token = request.json['token']
        if tdb.checkToken(actionname, token):
            return actualdelete()

    except Exception:
        pass
        
    newtoken = tdb.newToken(actionname)
    
    resp = {"message": "By deleting this action also the actions in the list will be deleted. Resend the request with the token to confirm." ,
            "dependencies": deplist,
            "token": newtoken}
    return make_response(jsonify(resp), 200)

def getSequences(request):
    seq = db.getSequences()
    return make_response(jsonify({"sequences": seq}), 200)

def flatSeq(token):
    seq = db.getSequence(token)
    
    return make_response(jsonify(seq["execSeq"]), 200)