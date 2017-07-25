from core.utils.httpUtils import post
import json
from core.databaseMongo import resultDB as rdb
from threading import Thread
import sys, traceback

class NodeInvoker:
    def __init__(self, ip):
        self.ip = ip

    def startExecution(self, request):
        ret = post(self.ip, "8080", "/internal/invoke", request, 50)
        return (ret.text, ret.status_code)

class AWSInvoker:
    def __init__(self, param):
        self.param = param

    def finalizeResult(self):
        if self.myID:
            rdb.insertResult(self.sessionID, self.myID,
                             json.loads(self.response))
            return ("OK", 200)
        else:
            return json.loads(self.response), 200

    def prepareInput(self):
        inParam = {}
        if not self.map:
            return self.param
        for newkey in self.map:
            s = self.map[newkey]
            list = s.split("/")
            refId = list[0]
            param = list[1]
            inParam[newkey] = rdb.getSubParam(self.sessionID, refId, param)
        return inParam


    def startExecution(self, request):
        from core.awsLambda.awsconnector import AwsActionInvoker
        self.map = request["action"]['map']
        self.sessionID = request['sessionID']
        self.myID = request["action"]['id']
        
        param = self.prepareInput()
        conn = AwsActionInvoker(request['action']['name'], param,
                                request['action']["actionClass"])
        r = conn.invoke()
        self.response = r["Payload"].read()
        if "FunctionError" in r:
            return (self.response, 500)

        return self.finalizeResult()

class InvokerThread(Thread):
    def __init__(self, invoker, action, sessionID):
        Thread.__init__(self)
        self.ret = (None, None)
        self.invoker = invoker
        self.action = action
        self.sessionID = sessionID

    def run(self):
        try:
            self.action["block"]
            request = {
                "type": "block",
                "sessionID" : self.sessionID,
                "param": None,
                "block": self.action["block"]
            }
        except KeyError:
            request = {
                "type": "action",
                "sessionID" : self.sessionID,
                "param": None,
                "action": self.action
            }
        try:
            self.ret = self.invoker.startExecution(request)
        except Exception as e:
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            self.ret = ({"error": str(e)}, 500)
