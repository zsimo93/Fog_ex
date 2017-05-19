import yaml

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


class NodeID():
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip

    def __repr__(self):
        return "id: " + self.id + " ip: " + self.ip


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


class Function(yaml.YAMLObject):
    yaml_tag = u'!Function'
    def __init__(self, name, cloud, timeout, language):
        self.name = name
        self.cloud = cloud
        self.timeout = timeout
        self.language = language

