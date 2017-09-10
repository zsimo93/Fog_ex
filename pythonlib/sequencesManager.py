from actionManager import ActionsManager
import requests

class SequencesManager(ActionsManager):
    def __init__(self, address):
        self.address = address

    def new(self, name, description, in_out, sequence):
        data = {
            "type": "sequence",
            "name": name,
            "description": description,
            "in/out": in_out,
            "sequence": sequence
        }
        resp = requests.post(self.address, json=data)
        return resp.status_code, resp.text

    # Functions: delete and list remains the same.
