import requests

class AWSManager():
    def __init__(self, address):
        self.address = address

    def new(self, accessKeyID, secretAccessID, ARN):
        data = {
            "accessKeyID": accessKeyID,
            "secretAccessID": secretAccessID,
            "ARN": ARN
        }
        resp = requests.post(self.address, json=data)
        return resp.status_code, resp.text

    def delete(self):
        resp = requests.delete(self.address)
        return resp.status_code, resp.text

    def check(self):
        resp = requests.get(self.address)
        return resp.status_code, resp.text
