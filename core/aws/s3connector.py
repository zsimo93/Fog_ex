import boto3
from core.databaseMongo import awsCredential
from datetime import datetime, timedelta

BUCKETNAME = 'my-userdata'

class FileOut():
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def read(self, size=-1):
        return self.data.read(size)

def getClient():
    cred = awsCredential.getCred()
    return boto3.client('s3',
                        aws_access_key_id=cred["accessKeyID"],
                        aws_secret_access_key=cred["secretAccessID"],
                        region_name="eu-central-1"
                        )

def getBucket():
    cred = awsCredential.getCred()
    s3 = boto3.resource('s3',
                        aws_access_key_id=cred["accessKeyID"],
                        aws_secret_access_key=cred["secretAccessID"],
                        region_name="eu-central-1"
                        )
    return s3.Bucket(BUCKETNAME)

def initBucket():
    s3 = getClient()
    try:
        s3.create_bucket(Bucket=BUCKETNAME,
                         CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
    except Exception as e:
        print e

def uploadFile(data, id, filename):
    delta = timedelta(seconds=1000)
    getBucket().upload_fileobj(data, id,
                               ExtraArgs={"Expires": datetime.utcnow() + delta,
                                          "Metadata": {"filename": filename}})


def download(fileID):
    resp = getClient().get_object(Bucket=BUCKETNAME, Key=fileID)

    fout = FileOut(resp["Body"], resp["Metadata"]["filename"])

    return fout


def deleteFile(id):
    getClient().delete_object(Bucket=BUCKETNAME, Key=id)
