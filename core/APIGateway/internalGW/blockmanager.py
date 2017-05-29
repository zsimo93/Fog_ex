from ActionManager import ActionManager
from threading import Thread
import json
"""
req = [
        {},
        {},
    ]
"""
class BlockManager():
    def __init__(self, block):
        actList = block['block']
        self.param = block['param']
        self.aManagers = []

        for action in actList:
            actionMan = ActionManager(action)
            thread = actionMan.startThreadContainer()
            self.aManagers.append((actionMan, thread))
            thread.start()


    def finalize(self):
        # save result in gridFS
        #  save(self.param)
        pass


    def run(self):
        for (manager, thread) in self.aManagers:
            manager.param = self.param
            thread.join()
            self.param = json.loads(manager.run())

        self.finalize()

        return json.dumps(self.param)
