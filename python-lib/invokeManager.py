import requests
from copy import deepcopy

class InvokeManager():
    def __init__(self, address, fileManager):
        self.address = address
        self.fileManager = fileManager

    def invoke(self, name, param, default_conf, except_conf={}, log=True, filePath="", paramID=""):
        newparam = deepcopy(param)
        if (filePath and paramID):
            code, text = self.fileManager.upload(filePath)
            if code == 200:
                newparam[paramID] = text

        data = {
            "param": newparam,
            "default": default_conf,
            "except": except_conf,
            "log": log
        }
        address = self.address + "/" + name

        resp = requests.post(address, json=data)

        return resp.status_code, resp.text
