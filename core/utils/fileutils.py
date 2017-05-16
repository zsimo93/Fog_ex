import zipfile

def unzip(extract, path):
    zip_ref = zipfile.ZipFile(path, 'r')
    zip_ref.extractall(extract)
    zip_ref.close()