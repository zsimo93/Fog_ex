#!thesis/api

from flask import Flask, request, abort
import core.APIGateway.nodes as nodes
import core.APIGateway.actions as actions
import core.APIGateway.sequences as sequences
import core.APIGateway.invoker as invoker
import core.APIGateway.aws as aws
import core.APIGateway.userfile as userfile
import core.APIGateway.internalGW.internal as internal
import os

def checkMaster():
    role = os.environ.get("TH_ROLE")
    return role == "MASTER"


app = Flask(__name__)

########################
@app.route('/api/nodes', methods=['POST'])
def newNode():
    if not checkMaster():
        return abort(404)
    return nodes.newNode(request)

@app.route('/api/nodes/<token>', methods=['DELETE'])
def deleteNode(token):
    if not checkMaster():
        return abort(404)
    return nodes.deleteNode(request, token)

@app.route('/api/nodes', methods=['GET'])
def getNodes():
    if not checkMaster():
        return abort(404)
    return nodes.getNodes(request)

@app.route('/api/nodes/reset', methods=["GET"])
def resetNodes():
    if not checkMaster():
        return abort(404)
    return nodes.reset()

#########################
@app.route('/api/actions', methods=['GET'])
def getActions():
    if not checkMaster():
        return abort(404)
    return actions.getActions(request)

@app.route('/api/actions', methods=['POST'])
def newAction():
    if not checkMaster():
        return abort(404)
    return actions.newAction(request)

@app.route('/api/actions/<token>', methods=['DELETE'])
def deleteAction(token):
    if not checkMaster():
        return abort(404)
    return actions.deleteAction(request, token)

#########################
@app.route('/api/sequences', methods=['GET'])
def getSequences():
    if not checkMaster():
        return abort(404)
    return sequences.getSequences(request)

@app.route('/api/sequences', methods=['POST'])
def newSequence():
    if not checkMaster():
        return abort(404)
    return sequences.newSequence(request)

@app.route('/api/sequences/<token>', methods=['DELETE'])
def deleteSeq(token):
    if not checkMaster():
        return abort(404)
    return sequences.deleteSequence(request, token)

@app.route('/api/<token>', methods=["GET"])
def flatSeq(token):
    return sequences.flatSeq(token)


########################
@app.route('/api/invoke', methods=['POST'])
def invoke():
    if not checkMaster():
        return abort(404)
    return invoker.invoke(request)

########################

@app.route('/api/aws', methods=["POST"])
def createAWSConnection():
    if not checkMaster():
        return abort(404)
    return aws.create(request)

@app.route('/api/aws', methods=["DELETE"])
def deleteAWSConnection():
    if not checkMaster():
        return abort(404)
    return aws.delete(request)

@app.route('/api/aws', methods=["GET"])
def checkAWSConnection():
    if not checkMaster():
        return abort(404)
    return aws.check(request)

########################

@app.route('/api/file/upload', methods=['POST'])
def uploadFile():
    if not checkMaster():
        return abort(404)
    return userfile.upload(request)

@app.route('/api/file/<token>', methods=["DELETE"])
def deleteFile(token):
    if not checkMaster():
        return abort(404)
    return userfile.delete(token)

@app.route('/api/file/<token>', methods=["GET"])
def downloadFile(token):
    if not checkMaster():
        return abort(404)
    return userfile.download(token)


########################
@app.route('/internal/invoke', methods=['POST'])
def intInvoke():
    return internal.invoke(request)

@app.route('/internal/delete/<token>', methods=['POST'])
def delFiles(token):
    return internal.delFiles(token, request)

@app.route('/internal/setup', methods=['POST'])
def setupVar():
    return internal.setup(request)

def run(debug):
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=debug)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
