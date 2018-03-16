
Add a node
~~~~~~~~~~~

We provide some example nodes in the `microhomie-nodes <https://github.com/microhomie/microhomie-nodes>`_ repository. Most of these nodes can be used out of the box to publish data. If you want to use a DHT22 sensor in example, copy the files ``__init__.py`` and ``dht22.py`` from ``homie/node`` to the ``lib/homie/node`` directory on your device. In the ``dht22.py`` file you see an example ``main.py`` as docstring. Copy this example to ``main.py`` on your device and on next reset it starts publishing temperature and humidity. In this example the DHT22 sensor is wired to GPIO PIN 4, on ESP8266 this is PIN D2.

You can also install nodes from PyPi:

>>> import upip
>>> upip.install('microhomie-nodes-dht22')