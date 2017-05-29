from core.databaseMongo import actionsDB as db
from core.gridFS import fileUtils
from core.container.dockerInterface import runContainer
from core.utils.httpUtils import post
from core.utils.fileUtils import deleteActionFiles
from requests import ConnectionError
from threading import Thread


"""request = {
    "name": "",
    "cpu": 0,
    "memory": 0,
    "param": {}
}"""


class ActionManager():
    def __init__(self, request, param={}):
        self.action = request['name']
        self.cpu = request['cpu']
        self.memory = request['memory']
        self.param = param
        
        fromDB = db.getAction(request['name'])
        self.timeout = fromDB['timeout']
        self.language = fromDB['language']


    def stopContainer(self):
        print self.cont.id
        self.cont.stop()
        self.cont.remove()
        print "done"  # log it instead
        deleteActionFiles(self.action)
        return


    def startCont(self):
        path = fileUtils.loadFile(self.action)
        self.cont , self.ip = runContainer("python-image",
                                           self.cpu, self.memory,
                                           path)

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
        self.response = r


    def error(self, exception):
        # add logging info
        self.response = str(exception)


    def run(self):
        try:
            self.makeRequest()

        except Exception, e:
            self.error(e)
        finally:
            Thread(target=self.stopContainer).start()

        return self.response


    def initAndRun(self):
        self.startCont()
        return self.run()