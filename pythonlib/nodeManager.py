import requests

class NodeManager():
    def __init__(self, address):
        self.address = address

    def new(self, ip, name, architecture, role, setup=False):
        data = {
            "type": "node",
            "setup": setup,
            "ip": ip,
            "architecture": architecture,
            "name": name,
            "role": role
        }
        resp = requests.post(self.address, json=data)
        return resp.status_code, resp.text

    def delete(self, name):
        address = self.address + "/" + name
        resp = requests.delete(address)
        return resp.status_code, resp.text

    def list(self):
        resp = requests.get(self.address)
        return resp.status_code, resp.text

    def reset(self):
        address = self.address + "/reset"
        resp = requests.get(address)
        return resp.status_code, resp.text
