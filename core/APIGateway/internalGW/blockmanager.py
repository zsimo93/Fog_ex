from actionmanager import ActionManager
from core.databaseMongo import localDB
import json

class BlockManager():
    def __init__(self, block, nlog, param, sessionID):
        self.actList = block
        self.localparams = {}
        self.aManagers = []
        self.param = param
        self.localiDs = []
        self.managerActionMap = {}
        self.sessionID = sessionID
        self.nlog = nlog
        self.loglist = []

        for action in self.actList:
            self.localiDs.append(action['id'])
            actionMan = ActionManager(action, nlog, map=action['map'],
                                      next=action['next'], sessionID=sessionID)

            if action["name"] not in self.managerActionMap:
                self.managerActionMap[action["name"]] = [actionMan]
                thread = actionMan.startThreadContainer()
                self.aManagers.append((actionMan, thread))
                thread.start()
            else:
                # same action found in block. reuse its container without releasing
                self.managerActionMap[action["name"]].append(actionMan)
                self.aManagers.append((actionMan, None))

        self.getData()

        self.result = {}

    def getData(self):
        for act in self.actList:
            for s in act["map"].values():
                vals = s.split("/")
                if vals[0] not in self.localiDs:
                    v = self.param[vals[0]][vals[1]]
                    self.localparams[vals[0] + "/" + vals[1]] = v

    def prepareSingleInput(self, map):
        inParam = {}
        for newKey in map:
            source = map[newKey]
            inParam[newKey] = self.localparams[source]
        return inParam

    def finalizeIntermediate(self, manager, result):

        def allLocal(next):
            for n in next:
                if n == "__out__":
                    # if out is needed for last return, save
                    return False
                if n not in self.localiDs:
                    return False
            return True

        for k in result:
            self.localparams[manager.myID + "/" + k] = result[k]
        if not allLocal(manager.next):
            self.result[manager.myID] = result

    def run(self):
        for (manager, thread) in self.aManagers:
            manager.param = self.prepareSingleInput(manager.map)

            if thread:
                thread.join()

            manager.setContainerMem()
            resp, error = manager.run()
            log = manager.log
            self.loglist += log
            newlogl = manager.loglength + len(log)
            actionName = manager.action
            amList = self.managerActionMap[actionName]
            amList.remove(manager)
            if len(amList) == 0:
                # no one else in the block requires the container.
                localDB.insertContainer(manager.action, manager.cont,
                                        manager.ip, newlogl)
            else:
                # redundant but np... set my container to all others.
                for am in amList:
                    am.cont = manager.cont
                    am.ip = manager.ip
                    am.loglength = newlogl
            if error:
                return (resp, 500)
            self.finalizeIntermediate(manager, json.loads(resp))

        if self.nlog:
            self.result["__log__"] = self.loglist

        return (json.dumps(self.result), 200)
