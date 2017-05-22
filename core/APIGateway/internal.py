from core.container import dockerInterface, invokePython
from flask import make_response
from core.databaseMongo.fs import fileUtils
from threading import Thread
from core.utils.httpUtils import get
from time import sleep


"""request.json = {
    "name": "",
    "language": "python",
    "cpu": 0,
    "memory": 0,
    "param": {}
}"""

def stop(cont):
    cont.stop()
    cont.remove()
    return

def invoke(request):
    req = request.json

    # sequences???

    # current node ARM or x86?

    r = "no match"
    if req['language'] == "python":
        try :
            cont , ip = dockerInterface.runContainer("python-image",
                                                     req['cpu'], req['memory'])
            file_path = fileUtils.loadFile(req['name'])

            sleep(0.5)

            invokePython.init(file_path, ip)
            r = invokePython.run(req['param'], ip)
            
            print r
            
        except Exception, e:
            r = str(e)
            print str(e)
        finally:
            Thread(target=stop, args=(cont, )).start()

        
    return make_response(r)



def fetch(token):
    pass