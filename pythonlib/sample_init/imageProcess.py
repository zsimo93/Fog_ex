from pythonlib.connectionManager import ConnectionManager

def init():
    cm = ConnectionManager("192.168.1.50")

    in_out = {"in": ["id1", "id2", "id3", "id4"], "out": ["retId"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/images/compose.py"
    r = cm.action.new("compose", "combine 4 images in one",
                      "python", "imageProc", in_out, "false", 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/images/rotate.py"
    r = cm.action.new("rotate", "rotate 180 degr the image",
                      "python", "imageProc", in_out, "false", 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/images/resize.py"
    r = cm.action.new("resize", "resize image to 200px",
                      "python", "imageProc", in_out, "false", 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/images/blackWhite.py"
    r = cm.action.new("blackWhite", "image to black and white",
                      "python", "imageProc", in_out, "false", 25, actionPath)
    print r

    in_out = {"in": ["id", "formatOut"], "out": ["retId"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/images/greyscale.py"
    r = cm.action.new("greyscale", "image to greyscale",
                      "python", "imageProc", in_out, "false", 25, actionPath)
    print r

    in_out = {"in": ["id", "format"], "out": ["retId"]}
    sequence = [{"id": "1",
                 "name": "resize",
                 "map": {"id": "param/id", "formatOut": "param/format"}},
                {"id": "2",
                 "name": "blackWhite",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "3",
                 "name": "greyscale",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "4",
                 "name": "rotate",
                 "map": {"id": "1/retId", "formatOut": "param/format"}},
                {"id": "5",
                 "name": "compose",
                 "map": {"id1": "1/retId", "id2": "2/retId", "id3": "3/retId", "id4": "4/retId"}}]
    r = cm.sequence.new("imageProc", "transform an image in 4 ways and combine in one",
                        in_out, sequence)
    print r
