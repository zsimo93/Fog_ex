from core.API import mainAPI
from core.database import nodeUtils, initSetup
import uuid

# initSetup.setup()
# mainAPI.run()

node = {
    'id': str(uuid.uuid1()),
    'name': 'raspi2',
    'ip': '192.168.1.10',
    'role': 'NODE',
    'architecture': 'ARM',
    'mqtt_Topic': 'node/raspi2',
    'cpu': 10.0,
    'memory': 1222.00
}

response = {'cpu': 13.5,
            'memory': 14507.30}

nodeUtils.updateResources('64fd8ea6-34cd-11e7-8d63-0800274927cb', response)
# utils.insertNode(node)
nodeUtils.updateNode('64fd8ea6-34cd-11e7-8d63-0800274927cb', 'ip', '192.168.1.33')
