import boto3
import json
import os
import time
from threading import Thread

cl = boto3.client("lambda",
                  aws_access_key_id='AWS_ACCESS_KEY_HERE',
                  aws_secret_access_key='AWS_SECRET_ACCESS_KEY_HERE',
                  region_name="eu-central-1"
                  )
s3 = boto3.client("s3",
                  aws_access_key_id='AWS_ACCESS_KEY_HERE',
                  aws_secret_access_key='AWS_SECRET_ACCESS_KEY_HERE',
                  region_name="eu-central-1"
                  )

path = r'C:\Users\Simone\Desktop\tst\Star-Wars.png'

class AwsActionInvoker(object):
    def __init__(self, name, param):
        self.name = name
        self.param = json.dumps(param)

    def invoke(self):
        response = cl.invoke(
            FunctionName=self.name,
            Payload=self.param,
        )
        return response


class AwsActionInvokerTh(Thread):
    def __init__(self, name, param):
        Thread.__init__(self)
        self.name = name
        self.param = json.dumps(param)

    def run(self):
        response = cl.invoke(
            FunctionName=self.name,
            Payload=self.param
        )
        self.id = json.loads(response["Payload"].read())["retId"]

def invoke(path=path, formatOut="PNG"):
    begin = time.time()
    id = os.path.basename(path)
    s3.upload_file(path, 'my-userdata', id)

    resp = AwsActionInvoker("aws-resize", {"id": id, "formatOut": "PNG"}).invoke()
    id1 = json.loads(resp["Payload"].read())["retId"]
    print id1

    t1 = AwsActionInvokerTh("aws-rotate", {"id": id1, "formatOut": "PNG"})
    t1.start()

    t2 = AwsActionInvokerTh("aws-bw", {"id": id1, "formatOut": "PNG"})
    t2.start()

    t3 = AwsActionInvokerTh("aws-greyscale", {"id": id1, "formatOut": "PNG"})
    t3.start()

    t1.join()
    id2 = t1.id
    print id2
    t2.join()
    id3 = t2.id
    print id3
    t3.join()
    id4 = t3.id
    print id4

    resp = AwsActionInvoker("aws-compose", {"id1": id1, "id2": id2, "id3": id3, "id4": id4}).invoke()
    idOut = json.loads(resp["Payload"].read())["retId"]

    print idOut

    s3.download_file('my-userdata', idOut, "aws-" + idOut)

    elapsed = time.time() - begin
    print elapsed
