from flask import Flask, request,make_response
import os
app = Flask(__name__)

@app.route("/")
def hello():
   return "Hello World from Flask"

@app.route('/api/actions/<token>', methods=['POST'])
def uploadAction(token):
    path = ("/home/pi")
    new_path = path + str(token)

    try:
        os.stat(new_path)
    except:
        os.mkdir(new_path)

    data = request.files['file']
    path = os.path.join(new_path, data.filename)

    print data.save(path)

    return make_response("OK", 200)

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)
