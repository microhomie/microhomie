
Setup WIFI for installation
-----------------------------

Microhomie handles WIFI setup for you, but for installation from PyPi you have to manual setup WIFI once from REPL.

>>> import network
>>> wlan = network.WLAN(network.STA_IF)
>>> wlan.active(True)
>>> wlan.connect('wifi-name', 'wifi-secret')
# wait a few seconds
>>> wlan.isconnected()  # test if wlan is connected
True
>>> wlan.ifconfig()  # get wlan interface config
('192.168.42.2', '255.255.255.0', '192.168.42.1', '192.168.42.1')





Configuration
-------------

Microhomie use a ``settings.py`` file to configure the device. See ``settings.example.py`` as an example. Modify this file for your needs and copy it to your device root directory as ``settings.py``.
