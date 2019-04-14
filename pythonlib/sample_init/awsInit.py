from pythonlib.connectionManager import ConnectionManager

cm = ConnectionManager("192.168.1.52")

def init():

    cm.aws.new('AWS_ACCESS_KEY_HERE',
               'AWS_SECRET_ACCESS_KEY_HERE',
               'arn:aws:iam::825346103633:role/lambdaBasic')
    """
    in_out = {"in": ["fileid"], "out": ["return"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/retFromFile.py"
    r = cm.action.new("getFileCloud", "get text file from fs",
                      "python", "base", in_out, "2", 5, actionPath)
    print r

    r = cm.action.new("getFile", "get text file from fs",
                      "python", "base", in_out, "0", 5, actionPath)
    print r

    in_out = {"in": ["text", "text2"], "out": ["return"]}
    actionPath = "C:/Users/Simone/workspace_thesis/sample_actions/concat.py"
    r = cm.action.new("concatCloud", "concatenate 2 strings",
                      "python", "base", in_out, "2", 2, actionPath)
    print r

    r = cm.action.new("concat", "concatenate 2 strings",
                      "python", "base", in_out, "0", 2, actionPath)
    print r

    in_out = {"in": ["text", "id"], "out": ["return"]}
    sequence = [{"id": "1",
                 "name": "getFile",
                 "map": {"fileid": "param/id"}},
                {"id": "2",
                 "name": "concatCloud",
                 "map": {"text": "1/return", "text2": "param/text"}},
                ]
    r = cm.sequence.new("s1", "...",
                        in_out, sequence)
    print r

    in_out = {"in": ["text", "id"], "out": {"4": "4/return", "3": "3/return"}}
    sequence = [{"id": "1",
                 "name": "getFile",
                 "map": {"fileid": "param/id"}},
                {"id": "2",
                 "name": "getFileCloud",
                 "map": {"fileid": "param/id"}},
                {"id": "3",
                 "name": "concat",
                 "map": {"text": "1/return", "text2": "2/return"}},
                {"id": "4",
                 "name": "concat",
                 "map": {"text": "3/return", "text2": "param/text"}},
                ]
    r = cm.sequence.new("s3", "...",
                        in_out, sequence)
    print r
"""


def remove():
    print cm.action.delete("getFileCloud", force=True)
    print cm.action.delete("getFile", force=True)
    print cm.action.delete("concatCloud", force=True)
    print cm.action.delete("concat", force=True)
