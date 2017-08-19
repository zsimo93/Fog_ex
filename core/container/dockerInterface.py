import docker
import commands

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def runContainer(name, memory, cpu_quota, path_dir):
    volumes = {
        path_dir: {"bind": "/action", "mode": "rw"}
    }

    a = client.containers.run(name,
                              volumes=volumes,
                              detach=True)
    if (memory):
        updateContainerMem(a.id, memory, cpu_quota)

    ip = getIP(a.id)

    return a.name, ip



def getIP(id):
    command = "docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + id

    ret = commands.getoutput(command)
    
    return ret

def killContainer(conId):
    c = client.containers.get(conId)
    c.kill()
    c.remove(v=True)

def updateContainerMem(contId, memory, cpu_quota):
    command = "docker update -m %s --cpus %s %s" % (str(memory) + "m",
                                                    str(cpu_quota), contId)

    commands.getoutput(command)

def pullImage(contName):
    client.images.pull(contName)

def delImage(contName):
    client.images.remove(image=contName)

def getContList():
    return client.containers.list()

def getUsedMem(contName):
    while True:
        try:
            stats = client.containers.get(contName).stats(decode=True, stream=False)
            return stats["memory_stats"]["usage"]
        except:
            continue
   
