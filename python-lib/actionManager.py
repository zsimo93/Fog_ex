import requests
import os
import json

class ActionsManager():
    def __init__(self, address):
        self.address = address

    def new(self, name, description, language,
            containerTag, in_out, cloud, timeout, filePath):
        data = {
            "type": "action",
            "name": name,
            "description": description,
            "language": language,
            "containerTag": containerTag,
            "in/out": in_out,
            "cloud": cloud,
            "timeout": timeout,
            "file": (os.path.basename(filePath), open(filePath, "rb"))
        }
        resp = requests.post(self.address, files=data)
        return resp.status_code, resp.text

    def list(self):
        resp = requests.get(self.address)
        return resp.status_code, resp.text

    def delete(self, actionName, force=False, token=None):
        address = self.address + "/" + actionName
        if (token):
            resp = requests.delete(address, json={"token": token})
        else:
            resp = requests.delete(address)

        if (resp.status_code == 304):
            if (force):
                token = json.loads(resp.text)["token"]

                resp = requests.delete(address, json={"token": token})

        return resp.status_code, resp.text
