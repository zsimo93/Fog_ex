#!thesis/api

from flask import Flask, request, make_response, abort
import nodes, actions, sequences, invoker, internalGW.internal as internal, aws
import os

def checkMaster():
    role = os.environ.get("TH_ROLE", "MASTER")
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

"""@app.route('/api/actions/<token>/invoke', methods=['POST'])
def invokeAction(token):
    return actions.invokeAction(request, token)
"""
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

"""@app.route('/api/sequences/<token>/invoke', methods=['POST'])
def invokeSeq(token):
    return sequences.invokeSequence(request, token)
"""

# #######################
@app.route('/api/invoke/<token>', methods=['POST'])
def invoke(token):
    if not checkMaster():
        return abort(404)
    return invoker.invoke(token, request)

# #######################

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

# #######################
@app.route('/internal/invoke', methods=['POST'])
def intInvoke():
    return internal.invoke(request)

@app.route('/internal/delete/<token>', methods=['POST'])
def delFiles(token):
    return internal.delFiles(token)

@app.route('/internal/setup', methods=['POST'])
def setupVar():
    return internal.setup(request)

def run():
    app.run(port=8080, threaded=True, debug=True)

if __name__ == '__main__':
    app.run(port=8080, threaded=True)
