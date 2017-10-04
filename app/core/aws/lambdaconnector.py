import boto3, json
from awspackage import PackageCreator
from core.databaseMongo import awsCredential
import s3connector
from io import BytesIO

def getClient():
    cred = awsCredential.getCred()
    return boto3.client('lambda',
                        aws_access_key_id=cred["accessKeyID"],
                        aws_secret_access_key=cred["secretAccessID"],
                        region_name="eu-central-1"
                        )

class AwsActionCreator(object):
    def __init__(self, name, language, description,
                 timeout, file, contTag):
        self.name = name
        self.file = file
        self.language = language + "2.7" if language == "python" else language
        self.description = description
        self.timeout = timeout
        self.package = self.initPackage(file, contTag)
        self.client = getClient()

    def initPackage(self, file, contTag):
        pc = PackageCreator(self.name, file, contTag)
        return pc.createPackage()

    def create(self):
        s3connector.getBucket().upload_fileobj(BytesIO(self.package), self.name + ".zip")
        actionClasses = {"small": 128,
                         "medium": 256,
                         "large": 512}

        for c in actionClasses:
            self.client.create_function(
                FunctionName=self.name + "_" + c,
                Runtime=self.language,
                Role=awsCredential.getCred()["ARN"],
                Handler='__handler__.my_handler',
                Code={
                    'S3Bucket': s3connector.BUCKETNAME,
                    'S3Key': self.name + ".zip"
                },
                Description=self.description,
                Timeout=self.timeout,
                MemorySize=actionClasses[c],
                Publish=True
            )

class AwsActionInvoker(object):
    def __init__(self, name, param, actClass, nlog):
        self.client = getClient()
        self.name = name
        self.param = json.dumps(param)
        self.actClass = actClass
        self.logType = "Tail" if nlog else "None"

    def invoke(self):
        response = self.client.invoke(
            FunctionName=self.name + "_" + self.actClass,
            Payload=self.param,
            LogType=self.logType
        )
        return response


class AwsActionDeletor(object):
    def __init__(self, name):
        self.client = getClient()
        self.name = name

    def delete(self):
        versions = ("small", "medium", "large")
        for v in versions:
            self.client.delete_function(
                FunctionName=self.name + "_" + v
            )
        s3connector.deleteFile(self.name + ".zip")
