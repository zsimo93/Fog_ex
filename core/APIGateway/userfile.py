from flask import make_response, send_file
from io import BytesIO
from core.gridFS import files

def upload(request):
    if 'file' not in request.files:
        return make_response("No file part")
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        return make_response('No selected file')

    fileid = files.saveUserData(file)

    return make_response(fileid, 200)

def delete(token):
    files.deleteUserData(token)

    return make_response("OK", 200)

def download(token):

    file = files.loadUserData(token)
    data = BytesIO(file.read())
    filename = file.filename
    mimetype = file.content_type
    return send_file(data, mimetype=mimetype,
                     attachment_filename=filename,
                     as_attachment=True)