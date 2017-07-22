from actionmanager import ActionManager
from core.databaseMongo import resultDB, localDB
import json
"""
param = {"text": "hello world"},
block =
    [
      {
        "name": "addStr",
        "cpu": 2,
        "memory": "250m",
        "language":
        "timeout"
      },
      {
        "name": "UpperDate",
        "cpu": 2,
        "memory": "250m"
        "language":
        "timeout"
      }
    ]
}
"""

class BlockManager():
    def __init__(self, block, sessionID):
        self.actList = block
        self.localparams = {}
        self.aManagers = []
        self.localiDs = []
        self.managerActionMap = {}
        self.sessionID = sessionID

        for action in self.actList:
            self.localiDs.append(action['id'])
            actionMan = ActionManager(action, map=action['map'],
                                      next=action['next'], sessionID=sessionID)
            
            if action["name"] not in self.managerActionMap:
                self.managerActionMap[action["name"]] = [actionMan]
                thread = actionMan.startThreadContainer()
                self.aManagers.append((actionMan, thread))
                thread.start()
            else:
                self.managerActionMap[action["name"]].append(actionMan)
                self.aManagers.append((actionMan, None))

        self.getData()


    def getData(self):
        for act in self.actList:
            for s in act["map"].values():
                vals = s.split("/")
                if vals[0] not in self.localiDs:
                    v = resultDB.getSubParam(self.sessionID, vals[0], vals[1])
                    self.localparams[vals[0] + "/" + vals[1]] = v

    def prepareSingleInput(self, map):
        inParam = {}
        for newKey in map:
            source = map[newKey]
            inParam[newKey] = self.localparams[source]
        return inParam

    def finalizeIntermediate(self, manager, result):
        
        def allLocal(next):
            if not next:
                # case of last action of a sequence. No next but need to save in DB
                return False
            for n in next:
                if n not in self.localiDs:
                    return False
            return True

        for k in result:
            self.localparams[manager.myID + "/" + k] = result[k]
        if not allLocal(manager.next):
            resultDB.insertResult(self.sessionID, manager.myID, result)



    def run(self):
        for (manager, thread) in self.aManagers:
            manager.param = self.prepareSingleInput(manager.map)
            
            if thread:
                thread.join()
            
            manager.setContainerMem()
            resp, error = manager.run()
            
            actionName = manager.action
            amList = self.managerActionMap[actionName]
            amList.remove(manager)
            if len(amList) == 0:
                # no one else in the block requires the container.
                localDB.insertContainer(manager.action, manager.cont,
                                        manager.ip)
            else:
                # redundant but np... set my container to all others.
                for am in amList:
                    am.cont = manager.cont
                    am.ip = manager.ip
            if error:
                return (resp, 500)
            self.finalizeIntermediate(manager, json.loads(resp))

        return ("OK", 200)
