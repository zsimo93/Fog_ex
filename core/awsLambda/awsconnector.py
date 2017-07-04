import boto3, json
from awspackage import PackageCreator
from core.databaseMongo import awsCredential

def getClient():
    cred = awsCredential.getCred()
    return boto3.client('lambda',
                        aws_access_key_id=cred["accessKeyID"],
                        aws_secret_access_key=cred["secretAccessID"],
                        region_name="eu-central-1"
                        )

class AwsActionCreator(object):
    def __init__(self, name, language, description,
                 timeout, file):
        self.name = name
        self.file = file
        self.language = language + "2.7" if language == "python" else language
        self.description = description
        self.timeout = timeout
        self.package = self.initPackage(file)
        self.client = getClient()

    def initPackage(self, file):
        pc = PackageCreator(self.name, file)
        return pc.createPackage()

    def create(self):
        response = self.client.create_function(
            FunctionName=self.name,
            Runtime=self.language,
            Role=awsCredential.getCred()["ARN"],
            Handler='__handler__.my_handler',
            Code={
                'ZipFile': self.package,
            },
            Description=self.description,
            # Timeout=self.timeout,
            # MemorySize=123,
            Publish=False
        )
        return response


class AwsActionInvoker(object):
    def __init__(self, name, param):
        self.client = getClient()
        self.name = name
        self.param = json.dumps(param)

    def invoke(self):
        response = self.client.invoke(
            FunctionName=self.name,
            Payload=self.param
        )
        return response


class AwsActionDeletor(object):
    def __init__(self, name):
        self.client = getClient()
        self.name = name

    def delete(self):
        self.client.delete_function(
            FunctionName=self.name
        )