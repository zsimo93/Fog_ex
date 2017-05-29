import docker
import commands

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def runContainer(name, cpu, memory, path_dir):
    volumes = {
        path_dir: {"bind": "/action", "mode": "rw"}
    }
    a = client.containers.run(name,
                              mem_limit=memory,
                              cpu_shares=cpu,
                              volumes=volumes,
                              detach=True)
    id = str(a.id)

    ip = getIP(id)

    return a, ip



def getIP(id):
    command = "docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + id

    ret = commands.getoutput(command)
    
    return ret
