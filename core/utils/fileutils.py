import zipfile, shutil, os

zip_tmp_dir = "/tmp"
actions_dir = "/actions"

def unzip(extract, path):
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(extract)
    zip_ref.close()


def zipFile(token):
    dir = shutil.make_archive(token, 'zip', os.path.join(actions_dir,token))
    shutil.move(dir, zip_tmp_dir)
    return os.path.join(zip_tmp_dir, token + '.zip')


def saveAction(token, data):
    new_path = actions_dir + str(token)
    try:
        os.stat(new_path)
    except:
        os.mkdir(new_path)
    path = os.path.join(new_path, data.filename)

    replica.replicate() # TODO implement

    return data.save(path)


def deleteActionFiles(path):
    shutil.rmtree(path)