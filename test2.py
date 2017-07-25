from copy import deepcopy

notInserted = set()

def fit(actions, nodes):
    couples = []
    actL = deepcopy(actions)[1:]

    a = actions[0]
    for n in nodes:
        actMem = a["memory"] * 1000000
        if actMem <= n["memory"]:
            nodeL = deepcopy(nodes)
            nodeL.remove(n)
            newNode = deepcopy(n)
            newNode["memory"] = n["memory"] - actMem
            nodeL.append(newNode)

            if len(actL) == 0:
                # No more actions to assign
                couples.append((a, n))
                
                try:
                    notInserted.remove(a["id"])
                except ValueError:
                    pass

                return couples

            ret = fit(actL, nodeL)
            if not ret:
                continue
            else:
                couples.append((a, n))
                couples += ret
                
                try:
                    notInserted.remove(a["id"])
                except ValueError:
                    pass

                return couples

    notInserted.add(a["id"])
    return None


actions = [
    {
        "id": "a1",
        "memory": 50
    },
    {
        "id": "a2",
        "memory": 75
    },
    {
        "id": "a3",
        "memory": 200
    }
]

nodes = [
    {
        "id": "n3",
        "memory": 130000000
    },
    {
        "id": "N1",
        "memory": 1000000
    },
    {
        "id": "N1",
        "memory": 100000000
    }
    
]

sep = []
coupling = fit(actions, nodes)

while notInserted:
    sep += [a for a in actions if a["id"] in notInserted]
    print sep

    parallelActions = [a for a in actions if a["id"] not in notInserted]
    notInserted = []
    coupling = fit(parallelActions, nodes)

print coupling