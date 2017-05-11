#!thesis/api

from flask import abort, make_response, jsonify
from core.common import Node
from core.database import utils
import uuid

def newNode(request):
    req = request.json

    if not request.json:
        abort(400)
    if not 'ip' in req or type(req['ip']) != unicode:
        return make_response(jsonify({'error': 'no ip'}), 400)
    if not "architecture" in req or type(req['architecture']) != unicode:
        return make_response(jsonify({'error': 'no arch'}), 400)

    node = Node(uuid.uuid4(), req['ip'], req['architecture'])
    
    return make_response(jsonify(node.__dict__), 200)

def deleteNode(request, token):
    
    res = utils.deleteNode(token)
    
    if not res:
        abort(404)

