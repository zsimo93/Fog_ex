from core.gridFS import files
from core.container.dockerInterface import runContainer
from core.databaseMongo import resultDB
from core.utils.httpUtils import post
from requests import ConnectionError
from threading import Thread
import json, traceback


"""request = {
    "name": "",
    "cpu": 0,
    "memory": 0,
    "param": {}
}
"""

class ActionManager():
    def __init__(self, request, param):
        self.action = request['name']
        self.memory = request['memory']
        self.map = map
        self.timeout = request['timeout']
        self.language = request['language']
        self.seqID = request["seqID"]
        self.myID = request["myID"]
        self.param = param

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
                                           self.memory,
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

    def run(self):
        try:
            self.makeRequest()
            self.error = False

            if self.code >= 400:
                self.error = True
        except Exception:
            tb = traceback.format_exc()
            self.error = True
            self.response = tb

        finally:
            Thread(target=self.stopContainer).start()

        return self.response, self.error

    def finalizeResult(self):
        if self.myID:
            id = self.seqID + "|" + self.myID
            resultDB.insertResult(id, json.loads(self.response))
            return ("OK", 200)
        else:
            return (json.loads(self.response), 200)

    def initAndRun(self):
        self.startCont()
        self.run()
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()
