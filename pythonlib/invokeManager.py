import requests
from copy import deepcopy

class InvokeManager():
    def __init__(self, address, fileManager):
        self.address = address
        self.fileManager = fileManager

    def invoke(self, name, param, default_conf_class, except_conf={}, log=True, filePath="", paramID="", optimise=True):
        newparam = deepcopy(param)
        if (filePath and paramID):
            code, text = self.fileManager.upload(filePath)
            if code == 200:
                newparam[paramID] = text

        data = {
            "name": name,
            "param": newparam,
            "default": {"actionClass": default_conf_class},
            "except": except_conf,
            "optimise": optimise,
            "log": log
        }
        resp = requests.post(self.address, json=data)

        return resp.status_code, resp.text
