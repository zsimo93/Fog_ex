import docker
import commands

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def runContainer(name, memory, path_dir):
    volumes = {
        path_dir: {"bind": "/action", "mode": "rw"}
    }

    if (memory):
        a = client.containers.run(name,
                                  mem_limit=str(memory) + "m",
                                  volumes=volumes,
                                  detach=True)
    else:
        a = client.containers.run(name,
                                  volumes=volumes,
                                  detach=True)

    id = str(a.id)

    ip = getIP(id)

    return a, ip



def getIP(id):
    command = "docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + id

    ret = commands.getoutput(command)
    
    return ret

def pull(contName):
    client.images.pull(contName)

def delImage(contName):
    client.images.remove(image=contName)
