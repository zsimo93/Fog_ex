from copy import deepcopy

def fitLessNodes(actions, nodes):
    couples = []
    actL = deepcopy(actions)[1:]

    a = actions[0]
    for n in nodes:
        print "try: " + a["id"] + " - " + n["id"]
        actMem = a["memory"] * 1000000
        if actMem <= n["memory"]:
            nodeL = deepcopy(nodes)
            nodeL.remove(n)
            #if len(nodes) < len(actions):
            newNode = deepcopy(n)
            newNode["memory"] = n["memory"] - actMem
            nodeL.append(newNode)

            if len(actL) == 0:
                # No more actions to assign
                couples.append((a, n))
                return couples

            ret = fitLessNodes(actL, nodeL)
            if not ret:
                continue
            else:
                couples.append((a, n))
                couples += ret
                return couples

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
        "memory": 100
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

print fitLessNodes(actions, nodes)