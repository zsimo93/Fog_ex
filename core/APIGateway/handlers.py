from core.utils.fileutils import uniqueName
from core.databaseMongo.sequencesDB import getSequence
from core.databaseMongo import resultDB as rdb, actionsDB, nodesDB
from threading import Thread
from requests import ConnectionError
from core.utils.httpUtils import post
import json


def giveMeHandler(param, default, configs, name, superSeqID=None,
                  myID=None, map={}):
    if not actionsDB.availableActionName(name):
        return ActionExecutionHandler(param, default, configs, name,
                                      superSeqID, myID, map)
    else:
        return ProcExecutionHandler(param, default, configs, name,
                                    superSeqID, myID, map)


class ExecutionHandler(object):
    def __init__(self, param, default, configs, superSeqID,
                 supermyID=None, map={}):
        self.param = param
        self.default = default
        self.configs = configs
        self.superSeqID = superSeqID
        self.supermyID = supermyID
        self.map = map

    def startThread(self):
        return Thread(target=self.start)

    def prepareInput(self):
        inParam = {}
        sources = self.map.keys()
        for s in sources:
            list = s.split("/")
            refId = list[0]
            param = list[1]
            newKey = self.map[s]
            if refId == "param":
                inParam[newKey] = self.param[param]
            else:
                inParam[newKey] = rdb.getSubParam(self.superSeqID, refId, param)
        return inParam

    def start(self):
        pass


class ActionRequest:
    def __init__(self, name, memory):
        self.name = name
        self.memory = memory

        fromDB = actionsDB.getAction(name)
        self.timeout = fromDB['timeout']
        self.language = fromDB['language']
        self.cloud = fromDB['cloud']

class RegInvoker:
    def __init__(self, ip):
        self.ip = ip

    def startExecution(self, request):
        ret = post(self.ip, "8080", "/internal/invoke", request, 10)
        return (ret.text, ret.status_code)


class AWSInvoker(ExecutionHandler):
    def __init__(self, param):
        self.param = param

    def finalizeResult(self):
        id = self.superSeqID + "|" + self.myID
        rdb.insertResult(id, json.loads(self.response))
        return ("OK", 200)

    def startExecution(self, request):
        from core.awsLambda.awsconnector import AwsActionInvoker
        self.map = request['map']
        self.superSeqID = request['seqID']
        self.myID = "" if not request['myID'] else request['myID']
        
        param = self.prepareInput()
        conn = AwsActionInvoker(request['action']['name'], param)
        response = conn.invoke()

        if "errorType" in response:
            return (response, 500)

        return self.finalizeResult()


class ActionExecutionHandler(ExecutionHandler):
    def __init__(self, param, default, configs, name, superSeqID,
                 supermyID, map):
        seqID = superSeqID
        if not superSeqID:
            seqID = uniqueName()
            rdb.insertResult(seqID + "|param", param)

        super(ActionExecutionHandler, self).__init__(param, default, configs,
                                                     seqID, supermyID, map)
        if configs and name in configs:
            conf = configs[name]
        else:
            conf = default

        self.action = ActionRequest(name, conf['memory'])

    def sortedAv(self, actionName):
        # sort the available nodes per cpu usage
        # avList = actionsDB.getAvailability(actionName)
        avList = nodesDB.allRes()

        return sorted(avList, key=lambda node: node['cpu'])


    def chooseNode(self):
        """
        Select the node with more free cpu and enought memory
        """
        req_mem = long(self.action.memory) * 1000000
        """
        if mem.endswith("m"):
            req_mem = long(mem[:-1] + "000000")
        elif mem.endswith("k"):
            req_mem = long(mem[:-1] + "000")
        elif mem.endswith("g"):
            req_mem = long(mem[:-1] + "000000000")
        """
        selected = None
        sortedAvList = self.sortedAv(self.action.name)

        if not sortedAvList:
            return ("localhost", RegInvoker("127.0.0.1"))

        for node in sortedAvList:
            if req_mem < node['memory']:
                # most free cpu and enought memory
                selected = node
                break
        if not selected:
            if self.action.cloud:
                return ("_cloud", AWSInvoker(self.param))
            else:
                selected = sortedAvList[0]
        return (selected, RegInvoker(nodesDB.getNode(selected['_id'])['ip']))

    def finalizeResult(self):
        resp = self.ret

        if not self.supermyID:
            # single action case. Return the result and delete from fs
            id = self.superSeqID + "|"
            result = rdb.getResult(id)
            del result['_id']
            resp = (json.dumps(result), 200)
            rdb.deleteAllRes(self.superSeqID)
        return resp

    def start(self):
        i = 0
        while(i < 2):
            try:
                name, invoker = self.chooseNode()

                request = {
                    "type": "action",
                    "map": self.map,
                    "seqID": self.superSeqID,
                    "myID": self.supermyID,
                    "action": self.action.__dict__
                }
                text, status_code = invoker.startExecution(request)
                if status_code >= 400:
                    self.ret = ({"error": text}, 500)
                    rdb.deleteAllRes(self.superSeqID)
                    return self.ret
                self.ret = (text, 200)
                return self.finalizeResult()
            except ConnectionError:
                nodesDB.deleteNode(name)
                rdb.deleteAllRes(self.superSeqID)
            except Exception, e:
                rdb.deleteAllRes(self.superSeqID)
                return ({"error": str(e)}, 500)
            else:
                break

        self.ret = ({"error": "2 nodes failed."}, 500)
        return self.ret


class ProcExecutionHandler(ExecutionHandler):
    def __init__(self, param, default, configs, name, superSeqID,
                 supermyID, map):
        super(ProcExecutionHandler, self).__init__(param, default, configs,
                                                   superSeqID, supermyID, map)
        self.name = name
        self.myID = uniqueName()
        self.process = getSequence(name)["process"]

        if map:
            newParam = self.prepareInput()
            self.param = newParam

        rdb.insertResult(self.myID + "|param", param)
        
    def cleanRes(self):
        rdb.deleteAllRes(self.myID)

    def finalizeResult(self):
        """
        take last result of the sequence and delete all the sequence intermediate results.
        If a subsequence, save again the result with the new ID and return None.
        Return the result otherwise.
        """
        idRes = self.myID + "|" + self.process[-1]["id"]
        res = rdb.getResult(idRes)
        del res["_id"]
        
        self.cleanRes()

        if self.superSeqID:
            newID = self.superSeqID + "|" + self.supermyID
            rdb.insertResult(newID, res)
            return (None, 200)
        
        return (json.dumps(res), 200)

    def start(self):
        for a in self.process:
            if a["id"] == "_parallel":
                handler = ParallelExecutionHandler(self.param, self.default,
                                                   self.configs, self.myID,
                                                   a["actions"])
            else:
                handler = giveMeHandler(self.param, self.default, self.configs,
                                        a["name"], self.myID,
                                        a["id"], a["map"])
            
            r, status_code = handler.start()
            if status_code >= 400:
                self.cleanRes()
                self.ret = (r, 500)
                return self.ret
            
        self.ret = self.finalizeResult()
        return self.ret


class ParallelExecutionHandler(ExecutionHandler):
    def __init__(self, param, default, configs, superSeqID, actions):
        super(ParallelExecutionHandler, self).__init__(param, default, configs,
                                                       superSeqID)
        self.actions = actions

    def start(self):
        handlers = []
        exTh = []
        for a in self.actions:
            hand = giveMeHandler(self.param, self.default, self.configs, a["name"],
                                 self.superSeqID, a["id"], a["map"])
            handlers.append(hand)
            thread = hand.startThread()
            thread.start()
            exTh.append(thread)

        for th in exTh:
            th.join()

        for h in handlers:
            if h.ret[1] >= 400:
                return (h.ret[0], 500)
                
        return ("OK", 200)