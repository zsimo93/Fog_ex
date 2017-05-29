#!thesis/api

from validator import validateSequence as validate, cleanUpSeq as clean
from core.databaseMongo import sequencesDB as db

def newSequence(request):

    valid, resp = validate(request)
    if not valid:
        return make_response(jsonify(resp), 400)

    name = resp.pop("name")
    
    if not db.availableSeqName(name):
        return make_response(jsonify({'error': name + " already in use"}), 406)

    # check all functions in list are available
    l = resp['sequence']
    a = db.checkSequence(l)
    if a:
        return make_response(jsonify({"error": "Action " + a + " not present"}), 400)
    
    resp = clean(resp)  # remove unwanted fields before storing in DB
    db.insertSequence(name, resp)
    return make_response(name, 201)


def deleteSequence(request, token):
    
    if not db.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    db.deleteSequence(token)
    return make_response("OK", 200)


def invokeSequence(request, token):
    
    if not db.availableSeqName(token):
        return make_response(jsonify({'error': "No sequence with name" + token}), 406)

    # TODO placement, invocation...
    pass

def getSequences(request):
    seq = db.getSequences()
    return make_response(jsonify({"sequences": seq}), 200)