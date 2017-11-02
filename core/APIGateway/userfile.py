from flask import make_response, send_file
from io import BytesIO
from core.gridFS import files
from core.databaseMongo import awsCredential as aws
from core.aws.s3connector import uploadFile as awsUpload, deleteFile as awsDelete

def upload(request):
    if 'file' not in request.files:
        return make_response("No file part", 400)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return make_response('No selected file', 400)

    fileid = files.saveUserData(file)
    if aws.checkPresence():
        file.seek(0)
        awsUpload(file, fileid, file.filename)
    return make_response(fileid, 200)

def delete(token):
    files.deleteUserData(token)
    if aws.checkPresence():
        awsDelete(token)
    return make_response("OK", 200)

def download(token):

    file = files.loadUserData(token)
    data = BytesIO(file.read())
    filename = file.filename
    mimetype = file.content_type
    return send_file(data, mimetype=mimetype,
                     attachment_filename=filename,
                     as_attachment=True)
