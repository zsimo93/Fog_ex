from core.container import dockerInterface, invokePython
from flask import make_response
from core.gridFS import fileUtils
from threading import Thread
from core.utils.httpUtils import post
from core.utils.fileUtils import deleteActionFiles
from time import sleep


"""request.json = {
    "name": "",
    "language": "python",
    "cpu": 0,
    "memory": 0,
    "param": {}
}"""

def stop(cont, name, ip):
    cont.stop()
    cont.remove()
    print "done"
    #deleteActionFiles(name)
    return

def invoke(request):
    req = request.json

    # sequences???

    # current node ARM or x86?

    r = "no match"
    if req['language'] == "python":
        try :
            path = fileUtils.loadFile(req['name'])
            #path_tmp = "/home/simone/action"
            cont , ip = dockerInterface.runContainer("python-image",
                                                     req['cpu'], req['memory'],
                                                     path)
            
            #wait = raw_input("wait to debug, enter to continue")
            sleep(0.5)
            r = post(ip, 8080, "/run", req['param'])
            print r
            
        except Exception, e:
            r = str(e)
            print str(e)
        finally:
            Thread(target=stop, args=(cont, req['name'], ip, )).start()

        
    return make_response(r)



def fetch(token):
    pass