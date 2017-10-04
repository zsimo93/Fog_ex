import uuid
import boto3
import botocore
from io import BytesIO
from datetime import datetime, timedelta
import os

BUCKETNAME = 'my-userdata'
bucket = boto3.resource('s3').Bucket(BUCKETNAME)
client = boto3.client('s3')

class NoFileException(Exception):
    pass

class WrongTypeException(Exception):
    pass

class FileOut():
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename

    def read(self, nbytes=-1):
        return self.data.read(nbytes)

class FileManager:

    def saveFile(self, file, filename):
        # Pass as file a io.BytesIO data type
        # or str

        id = str(uuid.uuid4())
        if (type(file) == BytesIO):
            toSave = file
        else:
            try:
                toSave = BytesIO()
                toSave.write(file)
            except:
                raise WrongTypeException("cannot save the data in the type given")

        delta = timedelta(seconds=1000)

        bucket.upload_fileobj(toSave, id,
                              ExtraArgs={"Expires": datetime.utcnow() + delta,
                                         "Metadata": {"filename": filename}})
        ids = os.environ.get("savedIds", "")
        if not ids:
            os.environ["savedIds"] = id
        else:
            os.environ["savedIds"] = ids + "|" + id
        return id

    def loadFile(self, fileID):
        try:
            resp = client.get_object(Bucket=BUCKETNAME, Key=fileID)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                raise NoFileException("No file with id " + str(fileID))
            else:
                raise
        else:
            fout = FileOut(resp["Body"], resp["Metadata"]["filename"])
            return fout
