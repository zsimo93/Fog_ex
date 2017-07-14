from flask import Flask, request, make_response, jsonify
from myapp import action

proxy = Flask(__name__)

@proxy.route("/run", methods=["POST"])
def run():
    args = request.json
    
    result = action(args)

    return make_response(jsonify(result), 200)
    
if __name__ == '__main__':
    proxy.run(host="0.0.0.0", port=8080)
