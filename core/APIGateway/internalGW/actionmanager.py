from core.gridFS import files
from core.container.dockerInterface import runContainer
from core.databaseMongo import resultDB
from core.utils.httpUtils import post
from requests import ConnectionError
from threading import Thread
import json


"""request = {
    "name": "",
    "cpu": 0,
    "memory": 0,
    "param": {}
}
"""


class ActionManager():
    def __init__(self, request, seqID, myID, param={}):
        self.action = request['name']
        self.cpu = request['cpu']
        self.memory = request['memory']
        self.param = param
        self.timeout = request['timeout']
        self.language = request['language']
        self.seqID = seqID
        self.myID = myID

    def stopContainer(self):
        while(True):
            try:
                self.cont.stop()
            except Exception:
                continue
            else:
                self.cont.remove()
                break
        return


    def startCont(self):
        self.path = files.loadFile(self.action)
        self.cont , self.ip = runContainer("python-image",
                                           self.cpu, self.memory,
                                           self.path)
    def startThreadContainer(self):
        return Thread(target=self.startCont)

    def makeRequest(self):
        while True:
                try:
                    r = post(self.ip, 8080, "/run", self.param, self.timeout)
                except ConnectionError:
                    continue
                else:
                    break

        self.response = r.text
        self.code = r.status_code

    def error(self, exception):
        # add logging info
        self.response = str(exception)


    def run(self):
        try:
            self.makeRequest()
            self.error = False

            if self.code >= 400:
                self.error = True
        except Exception, e:
            self.error = True
            self.error(e)

        finally:
            Thread(target=self.stopContainer).start()

        return self.response, self.error

    def finalizeResult(self):
        if self.seqID:
            resultDB.insertResult(self.seqID + "|" + self.myID, 
                                  json.loads(self.response))
            return ("OK", 200)
        else:
            return self.response, 200

    def initAndRun(self):
        self.startCont()
        self.run()
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()
