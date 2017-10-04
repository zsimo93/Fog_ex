from core.utils.httpUtils import post
import json
from threading import Thread
import sys, traceback
from core.gridFS.files import saveFilesFromAWS
import time

class NodeInvoker:
    def __init__(self, ip):
        self.ip = ip

    def startExecution(self, request, nlog):
        request["needlog"] = nlog
        ret = post(self.ip, "8080", "/internal/invoke", request, 100)
        return (ret.text, ret.status_code)

class AWSInvoker:
    def __init__(self):
        pass

    def finalizeResult(self, nlog):
        res = self.response
        begin = time.time()
        saving = saveFilesFromAWS(res["__savedIds__"])
        elapsed = time.time() - begin
        del res["__savedIds__"]
        if nlog:
            if saving:
                res["__log__"].append("Download from AWS in %s" % (repr(elapsed)))
        return res, 200

    def startExecution(self, request, nlog):
        from core.aws.lambdaconnector import AwsActionInvoker
        self.map = request["action"]['map']
        self.sessionID = request['sessionID']
        self.myID = request["action"]['id']
        self.param = request['param']

        conn = AwsActionInvoker(request['action']['name'], self.param,
                                request['action']["actionClass"], nlog)
        r = conn.invoke()
        payload = r["Payload"].read()
        self.response = json.loads(payload)
        if nlog:
            log = r["LogResult"]
            self.response["__log__"] = [self.myID + "AWS log : " + repr(log)]
        if "FunctionError" in r:
            return (self.response, 500)

        return self.finalizeResult(nlog)

class InvokerThread(Thread):
    def __init__(self, invoker, action, sessionID, param, actType, nlog):
        Thread.__init__(self)
        self.ret = (None, None)
        self.invoker = invoker
        self.action = action
        self.sessionID = sessionID
        self.param = param
        self.actType = actType
        self.nlog = nlog
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
            begin = time.time()
            self.ret = self.invoker.startExecution(request, self.nlog)
            self.elapsed = time.time() - begin
        except Exception as e:
            print '-' * 60
            traceback.print_exc(file=sys.stdout)
            print '-' * 60
            self.ret = ({"error": str(e)}, 500)
