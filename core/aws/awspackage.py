import zipfile, os
import subprocess
from core.utils.fileutils import uniqueName, deleteActionFiles as delFolder

class PackageCreator(object):
    abspath = "/tmp/aws/"

    def __init__(self, actionName, file, contTag):
        self.path = self.abspath + uniqueName() + "/"
        self.file = file
        self.filename = file.filename
        self.zipPath = self.path + "__handler__.zip"
        self.contTag = contTag

    def delFiles(self):
        delFolder(self.path[5:-1])

    def writeZip(self):
        self.file.save(self.zipPath)

    def writeFile(self):
        f = open(self.path + self.filename, "w")
        f.write(self.file.read())
        f.close()

    def createPackage(self):
        os.makedirs(self.path)

        in_zip = self.filename.endswith(".zip")

        if in_zip:
            name = "_main_"
        else:
            name = self.filename.split(".")[0]

        header = "from " + name + " import main\nimport os\n\n"
        funct = "def my_handler(event, context):\n"

        if self.contTag == "ffmpeg":
            funct += "    import subprocess\n"
            funct += "    subprocess.call(['cp', '/var/task/ffmpeg', '/tmp/'])\n"
            funct += "    subprocess.call(['chmod', '755', '/tmp/ffmpeg'])\n"

        funct += "    ret = main(event)\n"
        funct += "    ids = os.environ.get('savedIds', '')\n"
        funct += "    ret['__savedIds__'] = ids.split('|')\n"
        funct += "    return ret\n"

        program = header + funct
        hnd = open("__handler__.py", "w")
        hnd.write(program)
        hnd.close()

        if in_zip:
            self.writeZip()
            zf = zipfile.ZipFile(self.zipPath, mode='a')
            zf.external_attr = 644 << 16L
            zf.external_attr |= 444 << 16L
            zf.external_attr |= 0777 << 16L
            zf.write("./__handler__.py", arcname="__handler__.py")
            zf.write("./fileModule.py", arcname="fileModule.py")

        else:
            self.writeFile()
            zf = zipfile.ZipFile(self.zipPath, mode='w')
            zf.external_attr = 644 << 16L
            zf.external_attr |= 444 << 16L
            zf.external_attr |= 0777 << 16L
            zf.write("./__handler__.py", arcname="__handler__.py")
            zf.write("./fileModule.py", arcname="fileModule.py")
            zf.write(self.path + self.filename, self.filename)

        zf.close()

        if self.contTag == "ffmpeg":
            subprocess.call(["cd", "ffmpeg", "&", "zip", "-ur", self.zipPath, "./*"])
        elif self.contTag == "imageProc":
            subprocess.call(["cd", "ffmpeg", "&", "zip", "-ur", self.zipPath, "./*"])

        retFile = open(self.zipPath, "r")
        retBytes = retFile.read()
        retFile.close()

        self.delFiles()

        return retBytes
# --handler __handler__.my_handler \
