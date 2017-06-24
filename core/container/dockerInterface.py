import docker
import commands

# client = docker.DockerClient(base_url='unix://var/run/docker.sock')

client = docker.from_env()
def runContainer(name, cpu, memory, path_dir):
    volumes = {
        path_dir: {"bind": "/action", "mode": "rw"}
    }
    if (cpu and memory):
        a = client.containers.run(name,
                                  mem_limit=memory,
                                  cpu_shares=cpu,
                                  volumes=volumes,
                                  detach=True)
    elif (memory and not cpu):
        a = client.containers.run(name,
                                  mem_limit=memory,
                                  volumes=volumes,
                                  detach=True)
    elif (cpu and not memory):
        a = client.containers.run(name,
                                  cpu_shares=cpu,
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
