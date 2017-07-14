from core.databaseMongo import actionsDB
from core.utils.fileutils import uniqueName

class Block(object):
    def __init__(self, blockList):
        self.nodeList = blockList
        self.id = self.setId()
        self.next = self.getNext()
        self.prev = self.getPrev()

    def getPrev(self):
        return self.nodeList[0].prev
        
    def getNext(self):
        nextNodes = set()
        for node in self.nodeList:
            nextNodes |= set(node.next)

        return list(nextNodes)

    def setMemory(self, configs, default):
        for node in self.nodeList:
            node.setMemory(configs, default)

    def setId(self):
        return "BLOCK_" + self.nodeList[0].id

    def getIds(self):
        ids = []
        for item in self.nodeList:
            ids.append(item.id)
        return ids

    def __json__(self):
        jlist = []
        for a in self.nodeList:
            jlist.append(a.__json__())

        ret = {"id": self.id,
               "type": "block",
               "list": jlist}

        return ret


class Paral(Block):
    def __init__(self, parallelList):
        self.nodeList = parallelList
        self.id = self.setId()
        self.next = self.getNext()
        self.prev = self.getPrev()

    def setId(self):
        return "PARALLEL_" + self.nodeList[0].id

    def __json__(self):
        jlist = []
        for a in self.nodeList:
            jlist.append(a.__json__())

        ret = {"id": self.id,
               "type": "parallel",
               "list": jlist}
        return ret


class Act:
    def __init__(self, name, id=None, map={}, next=None, prev=None):
        self.id = id
        self.name = name
        self.map = map
        self.next = next
        self.prev = prev

        fromDB = actionsDB.getAction(name)
        self.timeout = fromDB['timeout']
        self.language = fromDB['language']
        self.cloud = fromDB['cloud']

    def __json__(self):
        ret = {
            "id": self.id,
            "type": "action",
            "name": self.name,
            "map": self.map,
            "next": self.next,
            "timeout": self.timeout,
            "language": self.language,
            "cloud": self.cloud,
        }

        return ret

class SequenceAnalizer:
    def __init__(self, fullSequence,):
        self.sequence = fullSequence

        self.doneIds = []
        self.finalProc = self.completeInfo()
        print self.finalProc
        self.finalProc = self.createBlocks()
        self.finalProc = self.createParallels()

    def __json__(self):
        jlist = []
        for a in self.finalProc:
            jlist.append(a.__json__())

        return jlist


    def completeInfo(self):
        # build a list af Act object, that contains all the information needed.
        # every node contains next, prev, id and the full action object
        l = []
        for act in self.sequence:
            id = act["id"]
            name = act["name"]
            map = act["map"]

            a = Act(name, id=id, map=map, next=act["next"], prev=act["prev"])

            l.append(a)
        return l

    def getNodeFromId(self, id):
        for node in self.finalProc:
            if node.id == id:
                return node
        return None

    def createParallels(self):
        newProcess = []
        for node in self.finalProc:
            if node.id not in self.doneIds:
                newProcess.append(self.computeParallelNode(node))
        return newProcess

    def computeParallelNode(self, node):
        def areParallel(prev1, prev2):
            return set(prev1) == set(prev2)

        others = [x for x in self.finalProc if x != node and x.id not in self.doneIds]
        parallelList = [node]
        for n in others:
            if areParallel(n.prev, node.prev):
                parallelList.append(n)
        if len(parallelList) == 1:
            ret = node
        else:
            ret = Paral(parallelList)
            self.doneIds += ret.getIds()

        return ret
    
    def createBlocks(self):
        newProcess = []
        for node in self.finalProc:
            if node.id not in self.doneIds:
                node = self.computeBlockNode(node)
                print node
                newProcess.append(node)
        return newProcess

    def computeBlockNode(self, node):
        blockList = self.getFollowingsInBlock(node)
        if len(blockList) == 1:
            ret = node
        else:
            ret = Block(blockList)
            self.doneIds += ret.getIds()

        return ret


    def getFollowingsInBlock(self, node):
        
        def containsParallel(nodes):
            # check if in a list of nodes' id there are parallels
            l = len(nodes)
            if l == 1:
                return False
            for ind1 in range(0, l):
                for ind2 in range(ind1, l):
                    node1 = self.getNodeFromId(nodes[ind1])
                    node2 = self.getNodeFromId(nodes[ind2])
                    if set(node1.prev) == set(node2.prev):
                        return True
            return False


        def isNext(prev1, id1, prev2):
            nset1 = set(prev1)
            nset2 = set(prev2)
            nset2.remove(id1)
            print nset1
            print prev2
            return nset2.issubset(nset1)

        block = [node]
        id = node.id
        nextNodes = node.next
        prevNodes = node.prev
        if containsParallel(nextNodes):
            pass
        else:
            for nid in nextNodes:
                nnode = self.getNodeFromId(nid)
                print nnode
                if isNext(prevNodes, id, nnode.prev):
                    block += self.getFollowingsInBlock(nnode)
        return block