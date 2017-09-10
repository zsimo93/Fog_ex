import requests
import os
import json
import encode_multipart

class ActionsManager():
    def __init__(self, address):
        self.address = address

    def new(self, name, description, language,
            containerTag, in_out, cloud, timeout, filePath):
        fields = {
            "type": "action",
            "name": name,
            "description": description,
            "language": language,
            "containerTag": containerTag,
            "in/out": json.dumps(in_out),
            "cloud": cloud,
            "timeout": str(timeout)
        }
        files = {
            "file": {'filename': os.path.basename(filePath), 'content': open(filePath, "rb").read()}
        }
        data, headers = encode_multipart.encode_multipart(fields, files)

        resp = requests.post(self.address, data=data, headers=headers)
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

        if (resp.status_code == 202):
            if (force):
                token = json.loads(resp.text)["token"]

                resp = requests.delete(address, json={"token": token})

        return resp.status_code, resp.text
