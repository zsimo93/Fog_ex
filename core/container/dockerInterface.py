import docker
import commands

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def runContainer(name, memory, path_dir):
    volumes = {
        path_dir: {"bind": "/action", "mode": "rw"}
    }

    if (memory):
        cont = client.containers.run(name,
                                     mem_limit=str(memory) + "m",
                                     volumes=volumes,
                                     detach=True)
    else:
        cont = client.containers.run(name,
                                     volumes=volumes,
                                     detach=True)
    id = str(cont.id)

    ip = getIP(id)

    return cont.name, ip


def getIP(id):
    command = "docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + id

    ret = commands.getoutput(command)

    return ret

def killContainer(conId):
    c = client.containers.get(conId)
    c.kill()
    c.remove(v=True)

def updateContainerMem(contId, memLimit):
    container = client.containers.get(contId)
    container.update(mem_limit=str(memLimit) + "m")

def pullImage(contName):
    client.images.pull(contName)

def delImage(contName):
    client.images.remove(image=contName)

def getLog(contName, logstart):
    return client.containers.get(contName).logs()[logstart:]

def getContList():
    return client.containers.list()

def getUsedMem(contName):
    while True:
        try:
            stats = client.containers.get(contName).stats(decode=True, stream=False)
            return stats["memory_stats"]["usage"]
        except:
            continue
