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
    def __init__(self, request, seqID, myID, map):
        self.action = request['name']
        self.cpu = request['cpu']
        self.memory = request['memory']
        self.map = map
        self.timeout = request['timeout']
        self.language = request['language']
        self.seqID = seqID
        self.myID = "" if not myID else myID
        self.param = self.prepareInput()

    def prepareInput(self):
        inParam = {}
        if not self.map:
            inParam = resultDB.getResult(self.seqID + "|param")
        else:
            for newKey in self.map:
                source = self.map[newKey]
                list = source.split("/")
                refId = list[0]
                param = list[1]
                inParam[newKey] = resultDB.getSubParam(self.seqID, refId, param)
        return inParam

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
        id = self.seqID + "|" + self.myID
        print id
        resultDB.insertResult(id, json.loads(self.response))
        return ("OK", 200)

    def initAndRun(self):
        self.startCont()
        self.run()
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()
