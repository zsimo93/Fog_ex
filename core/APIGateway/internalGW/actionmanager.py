from core.gridFS import files
from core.container.dockerInterface import runContainer, updateContainerMem, getLog
from core.databaseMongo import localDB
from core.utils.httpUtils import post
from requests import ConnectionError, ConnectTimeout
from threading import Thread
import traceback
import json, time


"""request = {
    "name": "",
    "cpu": 0,
    "memory": 0,
    "param": {}
}
"""

class ActionManager():
    def __init__(self, request, nlog, param=None, sessionID=None, map=None, next=[]):
        self.action = request['name']
        self.memory = request['memory']
        self.timeout = request['timeout']
        self.language = request['language']
        self.myID = request["id"]
        self.contTag = request["contTag"]
        self.nlog = nlog
        try:
            self.containerName = request["containerName"]
        except KeyError:
            pass
        self.sessionID = sessionID
        self.map = map
        self.param = param
        self.next = next
        self.loglist = []
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
            self.loglength = c[2]

        else:
            logStr = "%s - Starting new Container" % (self.myID)
            print logStr
            self.loglist.append(logStr)
            containerName = ""
            if self.language == "python":
                containerName = "zsimo/python-image:" + self.contTag
                # elif self.language == "docker":
                #     containerName = self.containerName
            else:
                containerName = "python"

            self.path = files.loadActionFile(self.action)
            self.cont, self.ip = runContainer(containerName,
                                              self.memory,
                                              self.path)
            self.loglength = 0
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
        if r:
            self.response = r.text
            self.code = r.status_code
        else:
            raise ConnectionError

    def run(self):
        # invoked directicly for blocks invocation and by action invocation
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

        log = getLog(self.cont, self.loglength)
        self.loglist.append(str(self.myID) + " - CONTAINER log:" + log)

        if not self.error:
            r = json.loads(self.response)
            begin = time.time()
            if files.uploadFilesToAWS(r["__savedIds__"]):
                elapsed = time.time() - begin
                self.loglist.append("%s - Uploading files to AWS in %s" %
                                    (self.myID, repr(elapsed)))
            del r["__savedIds__"]
            self.response = json.dumps(r)

        return self.response, self.error

    def finalizeResult(self):
        r = json.loads(self.response)
        if self.nlog:
            r["__log__"] = self.loglist
        return (json.dumps(r), 200)

    def initAndRun(self):
        # used for single action invocation
        self.startCont()
        self.run()
        newlogl = self.loglength + len(self.loglist[0]) - 15
        localDB.insertContainer(self.action, self.cont, self.ip, newlogl)
        if self.error:
            return (self.response, 500)
        return self.finalizeResult()

    def __repr__(self):
        return self.action + " - " + self.cont + " _ " + self.ip
