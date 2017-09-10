from actionManager import ActionsManager
from sequencesManager import SequencesManager
from fileManager import FileManager
from invokeManager import InvokeManager
from nodeManager import NodeManager
from awsManager import AWSManager

class ConnectionManager():
    def __init__(self, masterIP):
        port = 8080
        ip = masterIP
        baseAddress = "http://" + ip + ":" + str(port) + "/api"

        self.action = ActionsManager(baseAddress + "/actions")
        self.sequence = SequencesManager(baseAddress + "/sequences")
        self.file = FileManager(baseAddress + "/file")
        self.invoker = InvokeManager(baseAddress + "/invoke", self.file)
        self.node = NodeManager(baseAddress + "/nodes")
        self.aws = AWSManager(baseAddress + "/aws")
