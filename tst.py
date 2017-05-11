import psutil
import yaml
import io
import json


class Node(yaml.YAMLObject):
    yaml_tag = u'!Node'
    role='NODE'
    setup = True
    def __init__(self, name, ip, architecture, role='NODE', setup = True):
        self.name = name
        self.ip = ip
        self.architecture = architecture
        self.role = role
        self.setup = setup

    def __repr__(self):
        return "%s(%s,%s,%s,%s,%s)" % (
        self.__class__.__name__, self.name, self.ip, self.architecture, self.role, self.setup)

class Sequence(yaml.YAMLObject):
    yaml_tag = u'!Sequence'
    name = None
    sequence = list()
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence


class Cloud(yaml.YAMLObject):
    yaml_tag = u'!Cloud'
    def __init__(self, platform, link, username, password):
        self.platform = platform
        self.link = link
        self.username = username
        self.password = password

    def __repr__(self):
        return "%s(%s,%s,%s,%s)" % (
        self.__class__.__name__, self.platform, self.link, self.username, self.password)

class Function(yaml.YAMLObject):
    yaml_tag = u'!Function'
    def __init__(self, name, cloud, timeout, language):
        self.name = name
        self.cloud = cloud
        self.timeout = timeout
        self.language = language

    def __repr__(self):
        return "%s(%s,%s,%s,%s)" % (
        self.__class__.__name__, self.name, self.cloud, self.timeout, self.language)


print(psutil.cpu_percent(interval=0.1))
print(psutil.virtual_memory().available)
print(psutil.disk_usage("C:"))

stream = io.open('example.yml')
obj1, obj2, obj3, obj4= yaml.load_all(stream)

print obj1['nodes']
print obj1['cloud']

print json.dumps(obj2.__dict__)

print type(obj4.sequence[0])
