from core.databaseMongo.sequencesDB import getSequence
from core.databaseMongo import resultDB as rdb, actionsDB, nodesDB
from requests import ConnectionError
from core.utils.httpUtils import post
from threading import Thread
import time
from datetime import datetime
import json


def giveMeHandler(param, default, configs, name, sessionID):
    if not actionsDB.availableActionName(name):
        return ActionExecutionHandler(default, configs, name,
                                      sessionID, param)
    else:
        return SeqExecutionHandler(default, configs, name,
                                   sessionID, param)


def createAction(name, default, configs, myID, map, timeout,
                 language, cloud, next, containerName):
    action = {"name": name,
              'id': myID,  # None if single action execution
              "map": map}  # None if single action execution
    
    if configs and name in configs:
        conf = configs[name]
    else:
        conf = default
    action["memory"] = conf["memory"]

    if not myID:
        # single action execution. Retrieve information.
        fromDB = actionsDB.getAction(name)
        action["timeout"] = fromDB['timeout']
        action["language"] = fromDB['language']
        action["cloud"] = fromDB['cloud']
        try:
            action["containerName"] = fromDB["containerName"]
        except KeyError:
            pass
    else:
        action["timeout"] = timeout
        action["language"] = language
        action["cloud"] = cloud
        action["next"] = next
        action["containerName"] = containerName

    if action["cloud"]:
        action["actionClass"] = conf["actionClass"]

    return action

def calcBlockMemory(actList):
    memory = 0
    for a in actList:
        memory += a["memory"]
    return memory


class NodeInvoker:
    def __init__(self, ip):
        self.ip = ip

    def startExecution(self, request):
        ret = post(self.ip, "8080", "/internal/invoke", request, 10)
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


class NoResourceException(Exception):
    pass

class ActionExecutionHandler:
    def __init__(self, default, configs, name, sessionID, param=None,
                 myID=None, map=None, next=None, timeout=None,
                 language=None, cloud=None, containerName=None):

        self.param = param
        self.sessionID = sessionID
        self.action = createAction(name, default, configs, myID, map, timeout,
                                   language, cloud, next, containerName)
        self.logList = []

    def sortedCPU(self, avList):
        # sort the available nodes per cpu usage
        return sorted(avList, key=lambda node: node['cpu'])

    def sortedMem(self, avList):
        # sort the available nodes per free memory
        return sorted(avList, key=lambda node: node['memory'])

    def chooseNode(self):
        """
        Select the node with more free cpu and enought memory
        """
        req_mem = long(self.action["memory"]) * 1000000
        nodesRes = nodesDB.allRes()

        selected = None
        sortedNodes = self.sortedCPU(nodesRes)
        # sortedNodes = self.sortedMem(nodesRes)
        #   will take the node with less free memory
        #   that fit the requested memory

        attempt = 0
        while attempt < 3:
            # 3 attempts of finding a node with enought memory.
            # if no node and action no AWS execution, wait and retry later.

            for node in sortedNodes:
                if req_mem < node['memory']:
                    # most free cpu and enought memory
                    selected = node
                    return (selected["_id"], NodeInvoker(nodesDB.getNode(selected['_id'])['ip']))

            if not selected:
                if self.action["cloud"]:
                    return ("_cloud", AWSInvoker(self.param))
                else:
                    time.sleep(0.5)
                    attempt += 1
                    continue

        raise NoResourceException("Not enought memory resources in the " +
                                  "system to execute " + self.action["name"] +
                                  " using " + str(self.action["memory"]) + "MB")
    
    def startThreaded(self):
        return Thread(target=self.start)

    def start(self):
        i = 0
        while(i < 2):
            try:
                name, invoker = self.chooseNode()

                request = {
                    "type": "action",
                    "sessionID" : self.sessionID,
                    "param": self.param if not self.action["map"] else {},
                    "action": self.action
                }
                text, status_code = invoker.startExecution(request)
                if status_code >= 400:
                    self.ret = ({"error": text}, 500)
                    self.log("ERROR in remote execution")
                    return self.ret
                self.ret = (text, 200)
                self.log("EXECUTED in node " + name)
                return self.ret
            except ConnectionError:
                nodesDB.deleteNode(name)
            except Exception, e:
                self.log("Exception in local")
                return ({"error": str(e)}, 500)
            else:
                break

        self.ret = ({"error": "2 nodes failed."}, 500)
        return self.ret

    def log(self, message):
        ts = datetime.now().isoformat()
        actID = self.action["id"] if self.action["id"] else ""
        id = "ACTION " + actID + " " + self.action['name']
        logStr = ts + " - " + id + ": " + message
        self.logList.append(logStr)

class AsActionExecutionHandler(ActionExecutionHandler):
    def __init__(self, param, sessionID, action):
        self.param = param
        self.sessionID = sessionID
        self.action = action
        self.logList = []

class SeqExecutionHandler:
    def __init__(self, default, configs, name, sessionID, param):
        self.param = param
        self.sessionID = sessionID
        self.name = name
        self.default = default
        self.configs = configs

        s = getSequence(name)
        self.sequence = s["execSeq"]
        self.lastID = s["resultActionID"]
        rdb.insertResult(self.sessionID, "param", self.param)
        self.logList = []

        
    def cleanRes(self):
        rdb.deleteAllRes(self.sessionID)

    def finalizeResult(self):
        """
        take last result of the sequence and delete all the sequence intermediate results.
        Return the result.
        """
        res = rdb.getResult(self.sessionID, self.lastID)
        del res["_id"]
        
        self.cleanRes()

        return (json.dumps(res), 200)

    def start(self):
        self.log("Running")
        for a in self.sequence:
            if a["type"] == "parallel":
                handler = ParallelExecutionHandler(self.default, self.configs,
                                                   self.sessionID, a["list"])
            elif a["type"] == "block":
                handler = BlockExecutionHandler(self.default, self.configs,
                                                self.sessionID, a["list"])
            else:
                handler = ActionExecutionHandler(self.param, self.default,
                                                 self.configs, a["name"],
                                                 self.sessionID, a["id"],
                                                 a["map"], a["next"],
                                                 a["timeout"], a["language"],
                                                 a["cloud"], a["containerName"])

            try:
                r, status_code = handler.start()
                self.logList += handler.logList
                if status_code >= 400:
                    self.cleanRes()
                    self.ret = (r, 500)
                    return self.ret
                
            except Exception as e:
                self.cleanRes()
                self.log("Local Exception")
                return {"error": str(e)}, 500
        self.log("END")
        return self.finalizeResult()

    def log(self, message):
        ts = datetime.now().isoformat()
        id = "SEQUENCE " + self.name
        logStr = ts + " - " + id + ": " + message
        self.logList.append(logStr)
            
class ParallelExecutionHandler:
    def __init__(self, default, configs, sessionID, plist):
        self.default = default
        self.configs = configs
        self.sessionID = sessionID
        
        self.logList = []

        self.actList = []
        for a in plist:
            if a["type"] == "action":

                h = ActionExecutionHandler(self.default, self.configs,
                                           a["name"], self.sessionID,
                                           myID=a["id"], map=a["map"],
                                           timeout=a["timeout"],
                                           language=a["language"],
                                           cloud=a["cloud"], next=a["next"],
                                           containerName=a["containerName"])
                """
                ar = createAction(a["name"], self.default, self.configs,
                                  a["id"], a["map"], a["timeout"],
                                  a["language"], a["cloud"], a["next"],
                                  a["containerName"])
                """
            else:
                """
                block = {}
                blockList = []
                for b in a["list"]:
                    ar = createAction(b["name"], self.default, self.configs,
                                      b["id"], b["map"], b["timeout"],
                                      b["language"], b["cloud"], b["next"],
                                      b["containerName"])
                    blockList.append(ar)
                block["memory"] = calcBlockMemory(blockList)
                block["block"] = blockList

                """
                h = BlockExecutionHandler(self.default, self.configs,
                                          self.sessionID, a["list"])
            self.actList.append(h)

    def start(self):
        self.log("start execution")
        threads = []
        for h in self.actList:
            t = h.startThreaded()
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.log("end execution")

    def log(self, message):
        ts = datetime.now().isoformat()
        id = "PARALLEL"
        logStr = ts + " - " + id + ": " + message
        self.logList.append(logStr)

class BlockExecutionHandler(ActionExecutionHandler):
    def __init__(self, default, configs, sessionID, list):
        self.default = default
        self.configs = configs
        self.sessionID = sessionID
        self.ids = []
        self.logList = []
        
        self.blockList = []
        for a in list:
            ar = createAction(a["name"], self.default, self.configs,
                              a["id"], a["map"], a["timeout"],
                              a["language"], a["cloud"], a["next"],
                              a["containerName"])
            self.ids.append(a["id"])
            self.blockList.append(ar)

        self.memory = 0
        for ar in self.blockList:
            self.memory += ar["memory"]

    def chooseNode(self, actList):
        memory = calcBlockMemory(actList) * 1000000
        nodesRes = nodesDB.allRes()
        # sortedNodes = self.sortedMem(nodesRes)  take less memory that fits
        sortedNodes = self.sortedCPU(nodesRes)
        for node in sortedNodes:
            if memory < node['memory']:
                # most free cpu and enought memory
                return node["_id"], NodeInvoker(nodesDB.getNode(node['_id'])['ip'])

        return None, None

    def start(self):
        self.log("Executing block with actions: " + str(self.ids))
        
        while self.blockList:
            invoker = None
            
            if len(self.blockList) == 1:
                # one action left in the block. Execute as single action
                h = AsActionExecutionHandler(None, self.sessionID,
                                             self.blockList[0])
                text, code = h.start()
                self.logList += h.logList
                self.blockList = []
                return text, code

            else:
                name, invoker = self.chooseNode(self.blockList)
                if invoker:
                    # can execute the full block in a node. Do it!
                    payload = {
                        "type": "block",
                        "sessionID" : self.sessionID,
                        "block": self.blockList
                    }
                    text, code = invoker.startExecution(payload)
                    if code >= 400:
                        self.log("ERROR " + text)
                        return {"error": text}, 500

                    self.log("EXECUTE " + str(self.ids) + " on node " + name)
                    self.blockList = []
                    return "OK", 200

                else:
                    # cannot execute the full block. Try removing actions from
                    # end of block one at a time.
                    i = 0
                    while not invoker:
                        i -= 1
                        if len(self.blockList[:i]) == 1:
                            # if just one action, execute as single action.
                            h = AsActionExecutionHandler(None, self.sessionID,
                                                         self.blockList[0])
                            text, code = h.start()
                            self.logList += h.logList
                            if code >= 400:
                                return {"error": text}, 500

                            self.ids = self.ids[i:]
                            self.blockList = self.blockList[i:]
                            singleCase = True
                            break
                        else:
                            name, invoker = self.chooseNode(self.blockList[:i])
                            singleCase = False
                    
                    if not singleCase:
                        # execute the sub-block selected and reiterate with
                        # remaining actions in block

                        payload = {
                            "type": "block",
                            "sessionID" : self.sessionID,
                            "block": self.blockList[:i]
                        }
                        text, code = invoker.startExecution(payload)
                        if code >= 400:
                            self.log("ERROR " + text)
                            return {"error": text}, 500
                        
                        self.log("EXECUTE " + str(self.ids[:i]) + " on node " + name)
                        self.blockList = self.blockList[i:]
                        self.ids = self.ids[i:]
        
        self.log("END")
        return "OK", 200

    def log(self, message):
        ts = datetime.now().isoformat()
        id = "BLOCK"
        logStr = ts + " - " + id + ": " + message
        self.logList.append(logStr)