from pythonlib.connectionManager import ConnectionManager

cm = ConnectionManager("192.168.1.50")

def init():
    cm.aws.new('AKIAICLCF2RRAA2XJSEQ',
               'stalHM82bGS2Ftb4+1W2sQNJtUa/odNhoOlhcFKQ',
               'arn:aws:iam::825346103633:role/lambdaBasic')

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
    r = cm.action.new("concat", "concatenate 2 strings",
                      "python", "base", in_out, "2", 2, actionPath)
    print r

    in_out = {"in": ["text", "id"], "out": ["return"]}
    sequence = [{"id": "1",
                 "name": "getFile",
                 "map": {"id": "param/id"}},
                {"id": "2",
                 "name": "concat",
                 "map": {"text": "1/return", "text2": "param/text"}},
                ]
    r = cm.sequence.new("s1", "...",
                        in_out, sequence)
    print r

    in_out = {"in": ["text", "id"], "out": {"4": "4/return", "3": "3/return"}}
    sequence = [{"id": "1",
                 "name": "getFile",
                 "map": {"id": "param/id"}},
                {"id": "2",
                 "name": "getFileCloud",
                 "map": {"id": "param/id"}},
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
