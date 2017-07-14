import mainDB

db = mainDB.db

def addDependency(actionName, newdep):
    dep = db.dependencies
    val = dep.find_one_and_update({"_id": actionName},
                                  {"$addToSet": {"dep": newdep}})

def computeDep(seqName, sequence):
    for action in sequence:
        if action["id"] == "_parallel":
            listAct = action['actions']
            for a in listAct:
                addDependency(a["name"], seqName)
        else:
            addDependency(action["name"], seqName)

def getDependencies(actionName):
    dep = db.dependencies
    raw = dep.find_one({"_id": actionName})
    fullDep = set()
    fullDep.update(raw["dep"])

    for action in raw["dep"]:
        fullDep.update(getDependencies(action))

    return list(fullDep)
        
def removeDependencies(actionName):
    dep = db.dependencies

    for raw in dep.find():
        dep.find_one_and_update({"_id": raw["_id"]},
                                {"$pull": {"dep": actionName}})


