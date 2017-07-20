import zipfile, os
from core.utils.fileutils import uniqueName, deleteActionFiles as delFolder

class PackageCreator(object):
    abspath = "/tmp/aws/"

    def __init__(self, actionName, file):
        self.path = self.abspath + uniqueName() + "/"
        self.file = file
        self.filename = file.filename
        self.zipPath = self.path + "__handler__.zip"

    def delFiles(self):
        delFolder(self.path[5:-1])

    def writeZip(self):
        self.file.save(self.zipPath)

    def createPackage(self):
        os.makedirs(self.path)
        
        in_zip = self.filename.endswith(".zip")

        if in_zip:
            name = "_main_"
        else:
            name = self.filename.split(".")[0]
        
        header = "from " + name + " import main\n\n"
        funct = "def my_handler(event, context):\n    return main(event)\n"

        program = header + funct

        if in_zip:
            self.writeZip()
            zf = zipfile.ZipFile(self.zipPath, mode='a')
            zf.external_attr = 644 << 16L
            zf.external_attr |= 444 << 16L
            zf.writestr("__handler__.py", program)
            
        else:
            zf = zipfile.ZipFile(self.zipPath, mode='w')
            zf.external_attr = 644 << 16L
            zf.external_attr |= 444 << 16L
            zf.writestr("__handler__.py", program)
            zf.writestr(self.filename, self.file.stream.read())

        zf.close()

        retFile = open(self.zipPath, "r")
        retBytes = retFile.read()
        retFile.close()

        # self.delFiles()
        
        return retBytes



    # --handler __handler__.my_handler \