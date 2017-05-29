import urllib2
import urllib
import requests


def get(ip, port, path):
    url = "http://" + ip + ":" + str(port) + path

    response = requests.get(url)
    return response.text


def post(ip, port, path, payload, timeout):
    url = "http://" + ip + ":" + str(port) + path
    response = requests.post(url, json=payload, timeout=timeout)
    return response.text