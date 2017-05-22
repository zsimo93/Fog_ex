import urllib2
import urllib

def get(ip, port, path):
    url = "http://" + ip + ":" + str(port) + path
    print url

    #req = urllib2.Request(url)
    response = urllib.urlopen(url)
    return response.read()


def post(ip, port, path, payload):
    url = "http://" + ip + ":" + str(port) + path
    header = {'Content-Type': 'application/json'}
    req = urllib2.Request(url, payload, header)
    response = urllib2.urlopen(req) 
    return response.read()