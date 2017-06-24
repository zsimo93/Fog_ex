"""from ActionManager import ActionManager
from threading import Thread
from core.databaseMongo import resultDB
import json"""
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

"""class BlockManager():
    def __init__(self, block, param):
        actList = block
        self.param = param
        self.aManagers = []

        for action in actList:
            actionMan = ActionManager(action)
            thread = actionMan.startThreadContainer()
            self.aManagers.append((actionMan, thread))
            thread.start()


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
"""