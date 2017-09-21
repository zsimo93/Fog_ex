from core.databaseMongo import awsCredential
from validator import validateAWS
from flask import make_response, jsonify
from core.aws.s3connector import initBucket

def create(request):
    check, mess = validateAWS(request)
    if not check:
        return make_response(jsonify(mess), 400)

    accessKeyID = request.json["accessKeyID"]
    secretAccessID = request.json["secretAccessID"]
    arn = request.json["ARN"]

    retMsg = awsCredential.createCred(accessKeyID, secretAccessID, arn)
    initBucket()
    return make_response(retMsg, 200)


def delete(request):
    awsCredential.deleteCred()
    return make_response("OK", 200)


def check(request):
    if not awsCredential.checkPresence():
        return make_response("No aws credentials", 200)
    ret = {"accessKeyID": awsCredential.getCred()["accessKeyID"]}
    return make_response(jsonify(ret), 200)
