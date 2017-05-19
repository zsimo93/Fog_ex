import urllib2, urllib
from core.databaseRedis import nodesDB as db
# Thread???

def sendBinaryFile(token, binary=None):

    ips = map(lambda x: x.ip , db.getNodesIP) 

    file = open("C:/Users/Simone/workspace_thesis/downloads/file.zip", "r")

    url = "http://localhost:8080/api/actions/" + str(token)

    # make a string with the request type in it:
    method = "POST"
    # create a handler. you can specify different handlers here (file uploads etc)
    # but we go for the default
    handler = urllib2.HTTPHandler()
    # create an openerdirector instance
    opener = urllib2.build_opener(handler)
    # build a request
    data = urllib.urlencode(file)
    request = urllib2.Request(url, data=data)
    # add any other information you want
    request.add_header("Content-Type", 'application/zip')
    # overload the get method function with a small anonymous function...
    request.get_method = lambda: method
    # try it; don't forget to catch the result
    try:
        connection = opener.open(request)
    except urllib2.HTTPError, e:
        connection = e

    # check. Substitute with appropriate HTTP code.
    if connection.code == 200:
        data = connection.read()
    else:
        pass
        # handle the error case. connection.read() will still contain data
    # if any was returned, but it probably won't be of any use
