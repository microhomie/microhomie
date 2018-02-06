# Homie v2 MicroPython Framework

MicroPython implementation of the [Homie v2](https://github.com/marvinroger/homie) convention.

This project is in alpha stage.

## Examples

Please find multiple examples in the `examples` folder.

## Install

### Install from PyPi

We provide PyPi packages for easier installation on your device. Open the REPL from your device, make sure your device wlan is up and your device has access to the internet, import upip and install micropython-homie:

```python
>>> import upip
>>> upip.install('micropython-homie')
```

### Manual copy the files

To copy MicroHomie to your device use your favorite MicroPython remote shell like [rshell](https://github.com/dhylands/rshell), [mpfshell](https://github.com/wendlers/mpfshell) or [ampy](https://github.com/adafruit/ampy).

Create a directory `homie` on your device `lib` directory and copy the file `__init__.py` from the `homie` directory. Then create a `node` directory in `homie` and copy `__init__.py`, `led.py`, `simple.py` from the `homie/node` directory to the device.

Your file system structure should now look similar like this:

```
├── lib
|   ├── homie
│   |   ├── __init__.py
|   │   ├── node
│   │   |   ├── __init__.py
│   │   |   ├── led.py
│   │   |   ├── simple.py
├── boot.py
├── main.py
```

## Configuration

MicroHomie use a `settings.py` file to configure the device. See `settings.example.py` as an example. Modify this file for your needs and copy it to your device root directory as `settings.py`.


## ESP8266 example device

In this example we use the on-board LED from the ESP8266. Copy the `example-led.py` file from the `examples` diretory to your device and rename it to `main.py`.

You can now connect a MQTT client to your MQTT Broker an listen to the `homie/#` topic, or whatever you set as base topic.

Reset your ESP8266 and watch incoming MQTT messages.

The on-board LED status is reversed to the pin status. On start the on-board
LED is on. To turn it off send 'on' or 'toggle' via MQTT. Replace `<DEVICEID>` with the ID from the MQTT topic:

```shell
$ mosquitto_pub -t 'homie/<DEVICEID>/led/power/set' -m on
$ mosquitto_pub -t 'homie/<DEVICEID>/led/power/set' -m off
$ mosquitto_pub -t 'homie/<DEVICEID>/led/power/set' -m toggle
```


## Add a node

We provide some example nodes in the https://github.com/microhomie/micropython-homie-nodes repository. Most of these nodes can be used out of the box to publish data. If you want to use a DHT22 sensor in example, copy the files `__init__.py` and `dht22.py` from `homie/node` to the `lib/homie/node` directory on your device. In the `dht22.py` file you see an example `main.py` as docstring. Copy this example to `main.py` on your device and on next reset it starts publishing temperature and humidity. In this example the DHT22 sensor is wired to GPIO PIN 4, on ESP8266 this is PIN D2.

You have to setup/configure the network by yourself.

You can also install the `micropython-homie-nodes` package from PyPi with all the nodes we have for you:

```python
>>> import upip
>>> upip.install('micropython-homie-nodes')
```


### Local Development setup
You have to compile micropython with this guide https://github.com/micropython/micropython/wiki/Getting-Started

After that, you can install the required libraries.
```
micropython -m upip install micropython-umqtt.simple
micropython -m upip install micropython-logging
micropython -m upip install micropython-machine

```


### Simple node

In most cases you write your own node classes. But if you just want to test publishing or have a simple use case, you can use the `SimpleHomieNode` class. The `SimpleHomieNode` does not provide all homie properties, but can be used as a fast start, when you don't want to write anything in a class:

```python
import utime
import settings

from homie.node.simple import SimpleHomieNode
from homie import HomieDevice


homie_device = HomieDevice(settings)

n = SimpleHomieNode(node_type=b'dummy', node_property=b'value', interval=5)
n.value = 17

homie_device.add_node(n)
homie_device.publish_properties()

while True:
    homie_device.publish_data()
    n.value = utime.time()
    print(n)
    utime.sleep(1)
```
