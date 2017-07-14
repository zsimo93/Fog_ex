import mainDB

db = mainDB.db


def insertSequence(name, value):
    s = db.sequences
    dep = db.dependencies

    value["_id"] = name
    s.insert_one(value)

    depRecord = {"_id": name, "dep": []}
    dep.insert_one(depRecord)
    
    return name


def availableSeqName(name):
    s = db.sequences

    n = s.find({"_id" : name}).count()
    
    return n == 0


def getSequence(name):
    s = db.sequences

    return s.find_one({"_id" : name})


def deleteSequence(token):
    from actionsDB import deleteAction
    import dependenciesDB as depdb

    s = db.sequences
    dep = db.dependencies
    
    s.delete_one({"_id" : token})
    depdb.removeDependencies(token)

    deplist = dep.find_one_and_delete({"_id" : token})
    for dep in deplist["dep"]:
        if not availableSeqName(dep):
            deleteSequence(dep)
        else:
            deleteAction(dep)


def getSequences():
    s = db.sequences

    ret = []
    for k in s.find():
        try:
            del k["fullSeq"]
        except Exception:
            pass
        ret.append(k)

    return ret

def checkFields(actName, chklist, inOut):
    """
    used to check if the parameters in the chklist are in the
        input or output specification of the action actName.
    inOut is a "in" or "out" used to choose between the input or
        output parameters of the action.
    """
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
    a = db.actions
    s = db.sequences
   
    item = a.find_one({"_id" : token}) if a.find_one({"_id" : token}) else s.find_one({"_id" : token})

    lst = item["in/out"]["in"]

    for l in lst:
        if l not in param:
            return False, l

    return True, None

def checkSequence(sequence, in_out):
    # return the first incorrect name, none if all actions are ok
    from actionsDB import availableActionName as notPresent
    
    def checkAction(action, sequence):
        map = action["map"]
        name = action["name"]
        if notPresent(name) and availableSeqName(name):   # check if function is available
            return False, "Action '" + name + "' not found!"

        outP = map.values()
        inP = map.keys()
        
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
                for act in sequence:  # check if used an input of an action after this
                    if refId == act['id']:
                        refActName = act["name"]
                        ok, wrongfield = checkFields(refActName, param, "out")
                        if not ok:
                            return ok, "Field '" + wrongfield + "' not in the output list of action '" + refActName + "'"
                        check = True
                        break
                    elif act['id'] == action["id"]:    # case my id is encountered before refID
                        return False, "Action id '" + k + "' referenced before available"
                if not check:   # case the refID is not found in the sequence
                    return False, "The id '" + refId + "' to present in this sequence"
        return True, None

    
    ids = []
    for action in sequence:
        if action['id'] in ids:
            return False, "Repeated id " + str(action['id'])
        ids.append(action['id'])
        ok, errMsg = checkAction(action, sequence)
        if not ok:
            return ok, errMsg

    # check last action output match spec
    last = sequence[-1]
    
    ok, wrongfield = checkFields(last["name"], in_out["out"], "out")
    if not ok:
        return ok, ("Output params of the last action '" + last["name"] +
                    "' don't match the output sequence specification")

    return True, None
