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
    def __init__(self, request, param=None, sessionID=None, map=None, next=[]):
        self.action = request['name']
        self.memory = request['memory']
        self.timeout = request['timeout']
        self.language = request['language']
        self.myID = request["id"]
        try:
            self.containerName = request["containerName"]
        except KeyError:
            pass
        self.sessionID = sessionID
        self.map = map
        self.param = param
        self.next = next

    def stopContainer(self):
        while(True):
            try:
                self.cont.kill()
            except Exception:
                continue
            else:
                self.cont.remove()
                break
        print "done"
        return

    def startCont(self):
        containerName = ""
        if self.language == "python":
            containerName = "python-image"
        elif self.language == "docker":
            containerName = self.containerName
        else:
            containerName = "python"

        self.path = files.loadActionFile(self.action)
        self.cont , self.ip = runContainer(containerName,
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
            resultDB.insertResult(self.sessionID, self.myID,
                                  json.loads(self.response))
            return ("OK", 200)
        else:
            return (self.response, 200)

    def initAndRun(self):
        self.startCont()
        self.run()
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()
