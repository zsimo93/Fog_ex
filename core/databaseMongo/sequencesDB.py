from actionsDB import availableActionName as notPresent
import mainDB

def insertSequence(name, value):
    db = mainDB.db
    s = db.sequences

    value["_id"] = name
    s.insert_one(value)
    
    return name


def availableSeqName(name):
    db = mainDB.db
    s = db.sequences

    n = s.find({"_id" : name}).count()
    
    return n == 0


def getSequence(name):
    db = mainDB.db
    s = db.sequences

    return s.find_one({"_id" : name})


def deleteSequence(token):
    db = mainDB.db
    s = db.sequences
    
    s.remove({"_id" : token})


def getSequences():
    db = mainDB.db
    s = db.sequences

    ret = []
    for k in s.find():
        ret.append(k)

    return ret

def checkFields(actName, chklist, inOut):
    """
    used to check if the parameters in the chklist are in the
        input or output specification of the action actName.
    inOut is a "in" or "out" used to choose between the input or
        output parameters of the action.
    """
    db = mainDB.db
    a = db.actions
    s = db.sequences
   
    item = a.find_one({"_id" : actName}) if a.find_one({"_id" : actName}) else s.find_one({"_id" : actName})

    lst = item["in/out"][inOut]
    
    check = chklist
    if type(chklist) != list:
        check = [chklist]

    for l in check:
        if l not in lst:
            return False, l

    return True, None

def checkInputParam(token, param):
    db = mainDB.db
    a = db.actions
    s = db.sequences
   
    item = a.find_one({"_id" : token}) if a.find_one({"_id" : token}) else s.find_one({"_id" : token})

    lst = item["in/out"]["in"]

    for l in lst:
        if l not in param:
            return False, l

    return True, None

def checkSequence(process, in_out):
    # return the first incorrect name, none if all actions are ok

    def checkAction(action, process, in_parallel):
        map = action["map"]
        name = action["name"]
        if notPresent(name) and availableSeqName(name):   # check if function is available
            return False, "Action '" + name + "' not found!"

        outP = map.keys()
        inP = map.values()
        
        # check that input fields matches the ones specified
        ok, wrongfield = checkFields(name, inP, "in")
        if not ok:
            return ok, "Field '" + wrongfield + "' not in the input list of action '" + name + "'"

        for k in outP:
            list = k.split("/")
            refId = list[0]
            param = list[1]
            check = False
            if refId == "param":     # if referenced to param, check input spec
                if param not in in_out["in"]:
                    return False, "'" + k + " not in input sequence specification"
            else:
                for act in process:  # check if used an input of an action after this
                    if refId == act['id']:
                        refActName = act["name"]
                        ok, wrongfield = checkFields(refActName, param, "out")
                        if not ok:
                            return ok, "Field '" + wrongfield + "' not in the output list of action '" + refActName + "'"
                        check = True
                        break
                    elif act['id'] == "_parallel":    # case refId in a parallel block
                        listAct = act['actions']
                        for a in listAct:
                            if refId == a['id']:
                                if in_parallel:
                                    return False, ("In a parallel block you cannot reference the other actions in the block: '" +
                                                   action["id"] + "' -> '" + refId) + "'"
                                refActName = a["name"]
                                ok, wrongfield = checkFields(refActName, param, "out")
                                if not ok:
                                    return ok, "Field '" + wrongfield + "' not in the output list of action '" + refActName + "'"
                                check = True
                                break
                            elif a['id'] == action["id"]:    # case my id is encountered before refID
                                return False, "Action id '" + k + "' referenced before available"
                        if check:
                            break
                    elif act['id'] == action["id"]:    # case my id is encountered before refID
                        return False, "Action id '" + k + "' referenced before available"
                if not check:   # case the refID is not found in the process
                    return False, "The id '" + refId + "' to present in this process"
        return True, None

    
    for action in process:
        if action["id"] == "_parallel":
            in_parallel = True
            listAct = action['actions']
            for a in listAct:
                ok, errMsg = checkAction(a, process, in_parallel)
                if not ok:
                    return ok, errMsg
        else:
            in_parallel = False
            ok, errMsg = checkAction(action, process, in_parallel)
        if not ok:
            return ok, errMsg

    # check last action output match spec
    last = process[-1]
    if last["id"] == "_parallel":
        return False, "The process cannot end with a parallel block"

    ok, wrongfield = checkFields(last["name"], in_out["out"], "out")
    if not ok:
        return ok, ("Output params of the last action '" + last["name"] +
                    "' don't match the output process specification")

    return True, None
