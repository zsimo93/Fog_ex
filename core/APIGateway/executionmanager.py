 ##NOT USED

from core.utils.httpUtils import post
from core.utils.fileutils import uniqueName
from core.databaseMongo import actionsDB, nodesDB, sequencesDB
from requests import ConnectionError
from flask import make_response, jsonify
import json

class ActionRequest:
    def __init__(self, name, cpu, memory, id):
        self.name = name
        self.cpu = cpu
        self.memory = memory

        fromDB = actionsDB.getAction(name)
        self.timeout = fromDB['timeout']
        self.language = fromDB['language']

class SeqActionRequest(ActionRequest):
    def __init__(self, name, cpu, memory, seqID, actID):
        super(SeqActionRequest, self).init(name, cpu, memory)
        self.seqID = seqID
        self.actID = actID


class RequestHandler:
    def __init__(self, name, request):
        self.name = name
        self.param = request["param"]
        self.default = request["default"]
        try :
            self.configs = request['except']
        except KeyError:
            self.configs = None

    def isAction(self):
        # return True if the current request action name is an action
        return not actionsDB.availableActionName(self.name)

    def start(self):
        if self.isAction():
            man = ActionExecutionHandler(self.default, self.name, self.param)
        else:
            man = ProcExecutionHandler(self.param, self.default, self.configs,
                                       self.name)

        return man.run()


class ActionExecutionHandler:
    def __init__(self, config, name, param):
        self.action = ActionRequest(name, config['cpu'], config['memory'])
        self.param = param


    def sortedAv(self, actionName):
        # sort the available nodes per cpu usage
        avList = actionsDB.getAvailability(actionName)
        avResList = []

        for node in avList:
            res = nodesDB.getRes(node)
            del res["_id"]
            res["name"] = node

            avResList.append(res)

        return sorted(avResList, key=lambda node: node['cpu'])

    def chooseNode(self):
        """
        Select the node with more free cpu and enought memory
        """
        mem = self.action.memory

        if mem.endswith("m"):
            req_mem = long(mem[:-1] + "000000")
        elif mem.endswith("k"):
            req_mem = long(mem[:-1] + "000")
        elif mem.endswith("g"):
            req_mem = long(mem[:-1] + "000000000")

        selected = None

        # CLOUD ????
        sortedAvList = self.sortedAv(self.action.name)

        for node in sortedAvList:
            if req_mem < node['memory']:
                # most free cpu and enought memory
                selected = node
                break

        return selected, nodesDB.getNode(selected['name'])['ip']

    def startExecution(self, request, ip):
        ret = post(ip, "8080", "/internal/invoke", request, 5)
        return ret

    def run(self):
        i = 0
        while(i < 2):
            try:
                node, ip = self.chooseNode()
                request = {
                    "type": "action",
                    "param": self.param,
                    "action": self.action.__dict__
                }
                return (self.startExecution(request, ip), 200)

            except ConnectionError:
                nodesDB.deleteNode(node)
            else:
                break

        return (500)
            

class ProcExecutionHandler(ActionExecutionHandler):
    def __init__(self, param, default, configs, name, inSeqID=None):
        self.name = name
        self.param = param
        self.seqId = uniqueName()
        self.inSeqID = inSeqID
        self.setupSequence(default, configs)


    def setupSequence(self, default, configs):
        # retrieve all the actions configurations and constraints
        sequence = sequencesDB.getSequence(self.name)['sequence']
        
        sequenceObj = []
        for sublist in sequence:
            sublistAct = []
            for actionName in [x.encode('UTF8') for x in sublist]:
                if configs and actionName in configs:
                    conf = configs[actionName]
                else:
                    conf = default
                print actionName
                a = ActionRequest(actionName, conf['cpu'], conf['memory'])
                sublistAct.append(a)
            sequenceObj.append(sublistAct)

        self.remaining = sequenceObj


    def computeBlock(self):
        block = self.remaining.pop(0)

        avList = []

        for action in block:
            avList.append(actionsDB.getAvailability(action.name))

        intersection = avList[0]
        for i in range(1, len(avList)):
            intersection = [val for val in intersection if val in avList[i]]

        # if len(intersection) == 1:
        ip = nodesDB.getNode(intersection[0])['ip']

        # TODO

        blockdict = [act.__dict__ for act in block]

        return blockdict, ip


    def run(self):
        
        print self.remaining
        while len(self.remaining) != 0:
            blockList, ip = self.computeBlock()
            request = { "type": "block",
                        "sequenceId" : self.seqId,
                        "param": self.param,
                        "block": blockList }

            res = self.startExecution(request, ip)
            
            self.param = json.loads(res)


        return (jsonify(self.param), 200)
        
