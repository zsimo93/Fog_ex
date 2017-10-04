import zipfile, shutil, os
import uuid

tmp_dir = "/tmp"


def uniqueName(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.


class ReadError(Exception):
    pass


def _ensure_directory(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


def unzip(filename, extract_dir):

    if not zipfile.is_zipfile(filename):
        raise ReadError("%s is not a zip file" % filename)

    zip = zipfile.ZipFile(filename)
    try:
        for info in zip.infolist():
            name = info.filename

            # don't extract absolute paths or ones with .. in them
            if name.startswith('/') or '..' in name:
                continue

            target = os.path.join(extract_dir, *name.split('/'))
            if not target:
                continue

            _ensure_directory(target)
            if not name.endswith('/'):
                # file
                data = zip.read(info.filename)
                f = open(target, 'wb')
                try:
                    f.write(data)
                finally:
                    f.close()
                    del data
    finally:
        zip.close()
    


def deleteActionFiles(actName):
    path = tmp_dir + "/" + actName
    try:
        shutil.rmtree(path)
    except OSError:
        pass