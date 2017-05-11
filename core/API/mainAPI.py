#!thesis/api

from flask import Flask, request
import nodes, actions

app = Flask(__name__)

@app.route('/api/nodes', methods=['POST'])
def new():
    return nodes.newNode(request)

@app.route('/api/nodes/<token>', methods=['DELETE'])
def deleteNode(token):
    return nodes.deleteNode(request, token)

@app.route('/api/actions', methods=['POST'])
def newAction():
    return actions.newAction(request)

@app.route('/api/actions/<token>', methods=['POST'])
def uploadAction(token):
    return actions.uploadAction(request, token)

@app.route('/api/actions/<token>', methods=['PUT'])
def updateAction(token):
    return actions.updateAction(request, token)

@app.route('/api/actions/<token>', methods=['DELETE'])
def deleteAction(token):
    return actions.deleteAction(request, token)

@app.route('/api/actions/<token>/invoke', methods=['POST'])
def invokeAction(token):
    return actions.invokeAction(request, token)



def run():
    app.run(port=8080)

if __name__ == '__main__':
    app.run(port=8080)
