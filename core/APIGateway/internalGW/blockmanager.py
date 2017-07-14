from actionmanager import ActionManager
from core.databaseMongo import resultDB
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
        actList = block
        self.localparams = {}
        self.aManagers = []
        self.sessionID = sessionID

        for action in actList:
            actionMan = ActionManager(action)
            thread = actionMan.startThreadContainer()
            self.aManagers.append((actionMan, thread))
            thread.start()

    def prepareInput(self, map):
        inParam = {}
        if not map:
            inParam = resultDB.getResult(self.sessionID + "|param")
        else:
            for newKey in map:
                source = map[newKey]
                list = source.split("/")
                refId = list[0]
                param = list[1]
                inParam[newKey] = resultDB.getSubParam(self.sessionID, refId, param)
        return inParam

    def finalize(self):
        id = resultDB.insertResult(self.param)
        return id


    def run(self):
        for (manager, thread) in self.aManagers:
            manager.param = self.param
            thread.join()
            resp, error = manager.run()
            if error:
                return (error, 500)
            self.param = json.loads(resp)

        id = self.finalize()
        print id
        print self.param

        return json.dumps(self.param)
