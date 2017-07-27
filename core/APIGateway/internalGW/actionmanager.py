from core.gridFS import files
from core.container.dockerInterface import runContainer, updateContainerMem
from core.databaseMongo import localDB
from core.utils.httpUtils import post
from requests import ConnectionError, ConnectTimeout
from threading import Thread
import traceback


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
        self.contTag = request["contTag"]
        try:
            self.containerName = request["containerName"]
        except KeyError:
            pass
        self.sessionID = sessionID
        self.map = map
        self.param = param
        self.next = next
        self.cont = ""
        self.ip = ""

    def setContainerMem(self):
        updateContainerMem(self.cont, self.memory)

    def startCont(self):
        c = localDB.findContainer(self.action)

        if c:
            self.cont = c[0]
            self.ip = c[1]
            self.setContainerMem()

        else:
            containerName = ""
            if self.language == "python":
                containerName = "zsimo/python-image:" + self.contTag
            elif self.language == "docker":
                containerName = self.containerName
            else:
                containerName = "python"

            self.path = files.loadActionFile(self.action)
            self.cont , self.ip = runContainer(containerName,
                                               self.memory,
                                               self.path)
            localDB.insertInAll(self.cont, self.action)

    def startThreadContainer(self):
        return Thread(target=self.startCont)

    def makeRequest(self):
        i = 0
        while i < 10:
                try:
                    r = post(self.ip, 8080, "/run", self.param, self.timeout)
                except ConnectionError:
                    i += 1
                    print "BLOCKING"
                    r = None
                    continue
                except ConnectTimeout:
                    raise ConnectTimeout
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
        except ConnectTimeout as e:
            self.error = True
            self.response = str(e)
        except Exception:
            tb = traceback.format_exc()
            self.error = True
            self.response = tb

        return self.response, self.error

    def finalizeResult(self):
        return (self.response, 200)

    def initAndRun(self):
        self.startCont()
        self.run()
        localDB.insertContainer(self.action, self.cont, self.ip)
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()

    def __repr__(self):
        return self.action + " - " + self.cont + " _ " + self.ip