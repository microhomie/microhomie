# Homie v2 MicroPython Framework

MicroPython implementation of the [Homie v2](https://github.com/marvinroger/homie) convention.

This project is in alpha stage.

## Examples

Please find multiple examples in the `examples` folder.

## Device setup

Create a directory `homie` on your device and copy the file `__init__.py` from the `homie` directory. From the `repl` you can now setup your homie device:

```
>>> from homie import HomieDevice
>>> CONFIG = {'mqtt': {'broker': 'localhost'}}
>>> homie = HomieDevice(CONFIG)
```

When your device is setup you start publishing the device and later node properties:

```
homie.publish_properties()
```

From now on you have to setup a loop to continuous publish device and node data:

```
>>> import utime
>>> while True:
...     homie.publish_data()
...     utime.sleep(1)
```

If you also listen to topics you have to check for new messages:

```
homie.mqtt.check_msg()
```


### Device configuration

Device class is configured with an dictionary. Default device configuration:

```python
CONFIG = {
    'mqtt': {
        'broker': '127.0.0.1',
        'port': 0,
        'user': None,
        'pass': None,
        'keepalive': 60,
        'ssl': False,
        'ssl_params': {},
        'base_topic': b'homie'
    },
    'device': {
        'id': ubinascii.hexlify(machine.unique_id()),
        'name': b'mydevice',
        'fwname': b'uhomie',
        'fwversion': __version__,
        'localip': bytes(network.WLAN(0).ifconfig()[0], 'utf-8'),
        'mac': ubinascii.hexlify(network.WLAN(0).config('mac'), ':'),
        'platform': bytes(sys.platform, 'utf-8'),
        'stats_interval': 60
    }
}
```


## Add a node

We provide some example nodes in the `homie/node` directory. Most of these nodes can be used out of the box to publish data. If you want to use a DHT22 sensor in example, copy the files `__init__.py` and `dht22.py` from `homie/node` to the same directory on your device. In the `dht22.py` file you see an example `main.py` as docstring. Copy this example to `main.py` on your device and on next reset it starts publishing temperature and humidity. In this example the DHT22 sensor is wired to GPIO PIN 4, on ESP8266 this is PIN D2.

You have to setup/configure the network by yourself.


### Local Development setup
You have to compile micropython with this guide https://github.com/micropython/micropython/wiki/Getting-Started

After that, you can install the required libraries.
```
micropython -m upip install micropython-umqtt.simple
micropython -m upip install micropython-umqtt.robust
micropython -m upip install micropython-logging
micropython -m upip install micropython-machine

```


### Simple node

In most cases you write your own node classes. But if you just want to test publishing or have a simple use case, you can use the `SimpleHomieNode` class. The `SimpleHomieNode` does not provide all homie properties, but can be used as a fast start, when you don't want to write anything in a class:

```python
import utime

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice

CONFIG = {
    'mqtt': {
        'broker': '127.0.0.1',
    },
}

homie = HomieDevice(CONFIG)

n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
n.value = 17

homie.add_node(n)
homie.publish_properties()

while True:
    homie.publish_data()
    n.value = utime.time()
    print(n)
    utime.sleep(1)
```
