from threading import Thread
import docker
import commands
import urllib
from time import sleep


client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def get(ip, port, path):
    url = "http://" + ip + ":" + str(port) + path
    print url

    #req = urllib2.Request(url)
    response = urllib.urlopen(url)
    return response.read()

def runContainer(name, cpu, memory):
    a = client.containers.run(name,
                              mem_limit=memory,
                              # cpu_shares=cpu,
                              detach=True)
    id = str(a.id)

    ip = getIP(id)

    return a, ip

def stop(cont):
    cont.stop()
    cont.remove()
    return


def getIP(id):
    command = "docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + id

    ret = commands.getoutput(command)
    
    return ret



def invoke():
    r = "no match"

    try :
        cont , ip = runContainer("python-image", 2, "150m")
        file_path = fileUtils.loadFile(req['name'])

        sleep(0.2)
        invokePython.init(file_path, ip)
        r = invokePython.run(req['param'], ip)
        
#        r = get(str(ip), 8080, "/run")
        
    except Exception, e:
        r = str(e)
    finally:
        Thread(target=stop, args=(cont, )).start()

        
    return r

print invoke()