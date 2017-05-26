#!thesis/api

from flask import Flask, request
import nodes, actions, sequences, internal

app = Flask(__name__)

########################
@app.route('/api/nodes', methods=['POST'])
def newNode():
    return nodes.newNode(request)

@app.route('/api/nodes/<token>', methods=['DELETE'])
def deleteNode(token):
    return nodes.deleteNode(request, token)

@app.route('/api/nodes', methods=['GET'])
def getNodes():
    return nodes.getNodes(request)

#########################
@app.route('/api/actions', methods=['GET'])
def getActions():
    return actions.getActions(request)

@app.route('/api/actions', methods=['POST'])
def newAction():
    return actions.newAction(request)

"""@app.route('/api/actions/<token>', methods=['POST'])
def uploadAction(token):
    return actions.uploadAction(request, token)"""

"""@app.route('/api/actions/<token>', methods=['GET'])
def downloadAction(token):
    return actions.downloadAction(token)"""

@app.route('/api/actions/<token>', methods=['PUT'])
def updateAction(token):
    return actions.updateAction(request, token)

@app.route('/api/actions/<token>', methods=['DELETE'])
def deleteAction(token):
    return actions.deleteAction(request, token)

@app.route('/api/actions/<token>/invoke', methods=['POST'])
def invokeAction(token):
    return actions.invokeAction(request, token)

#########################
@app.route('/api/sequences', methods=['GET'])
def getSequences():
    return sequences.getSequences(request)

@app.route('/api/sequences', methods=['POST'])
def newSequence():
    return sequences.newSequence(request)

@app.route('/api/sequences/<token>', methods=['DELETE'])
def deleteSeq(token):
    return sequences.deleteSequence(request, token)

@app.route('/api/sequences/<token>/invoke', methods=['POST'])
def invokeSeq(token):
    return sequences.invokeSequence(request, token)

# ######################## TODO ###############################
@app.route('/internal/invoke', methods=['POST'])
def function():
    return internal.invoke(request)

@app.route('/internal/result/<token>', methods=['GET'])
def function2(token):
    return internal.fetch(token)


def run():
    app.run(port=8080, threaded=True, debug=True)

if __name__ == '__main__':
    app.run(port=8080)
