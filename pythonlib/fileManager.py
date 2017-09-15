import os
import requests
from io import BytesIO

class FileManager():
    def __init__(self, address):
        self.address = address

    def upload(self, filePath):
        data = {"file": (os.path.basename(filePath), open(filePath, "rb"))}
        resp = requests.post(self.address + "/upload", files=data)
        return resp.status_code, resp.text

    def download(self, fileId):
        address = self.address + "/" + fileId
        resp = requests.get(address)
        buff = BytesIO()

        for chunk in resp.iter_content(chunk_size=255):
            if chunk:
                buff.write(chunk)
        buff.seek(0)
        return resp.status_code, buff, resp.headers["Content-Type"]

    def delete(self, fileId):
        address = self.address + "/" + fileId
        resp = requests.delete(address)
        return resp.status_code, resp.text
