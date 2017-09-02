import fileModule

def main(args):
    filename = args['fileid']

    fm = fileModule.FileManager()
    data = fm.loadFile(filename)

    return{"return": data.read()}
