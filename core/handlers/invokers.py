from core.utils.httpUtils import post
import json
from threading import Thread
import sys, traceback
from core.gridFS.files import saveFilesFromAWS

class NodeInvoker:
    def __init__(self, ip):
        self.ip = ip

    def startExecution(self, request):
        ret = post(self.ip, "8080", "/internal/invoke", request, 100)
        return (ret.text, ret.status_code)

class AWSInvoker:
    def __init__(self):
        pass

    def finalizeResult(self):
        res = json.loads(self.response)
        saveFilesFromAWS(res["__savedIds__"])
        del res["__savedIds__"]

        return res, 200

    def startExecution(self, request):
        from core.aws.lambdaconnector import AwsActionInvoker
        self.map = request["action"]['map']
        self.sessionID = request['sessionID']
        self.myID = request["action"]['id']
        self.param = request['param']

        conn = AwsActionInvoker(request['action']['name'], self.param,
                                request['action']["actionClass"])
        r = conn.invoke()
        self.response = r["Payload"].read()
        if "FunctionError" in r:
            return (self.response, 500)

        return self.finalizeResult()

class InvokerThread(Thread):
    def __init__(self, invoker, action, sessionID, param, actType):
        Thread.__init__(self)
        self.ret = (None, None)
        self.invoker = invoker
        self.action = action
        self.sessionID = sessionID
        self.param = param
        self.actType = actType
        del self.action["type"]

    def run(self):
        if self.actType == "block":
            request = {
                "type": "block",
                "sessionID": self.sessionID,
                "param": self.param,
                "block": self.action["block"]
            }
        else:
            request = {
                "type": "action",
                "sessionID": self.sessionID,
                "param": self.param,
                "action": self.action
            }
        try:
            self.ret = self.invoker.startExecution(request)
        except Exception as e:
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            self.ret = ({"error": str(e)}, 500)
