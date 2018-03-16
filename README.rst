==========
Microhomie
==========

|build-status| |pypi|


A MicroPython implementation of the `Homie <https://github.com/marvinroger/homie>`_ MQTT convention version ``2.1.0``.

This project is in beta stage.


Known issues
------------

* SSL connection problems at least with ESP8266
* In lost of Wifi connection, there is a chance MQTT qos==1 will hang forever


Install
-------

You can get the detailed installation instructions here: http://microhomie.readthedocs.io/



Local Development setup
-----------------------

You have to compile micropython with this guide https://github.com/micropython/micropython/wiki/Getting-Started

After that, you can install the required libraries.

.. code-block:: shell

    micropython -m upip install micropython-umqtt.simple
    micropython -m upip install micropython-logging
    micropython -m upip install micropython-machine







.. |build-status| image:: https://readthedocs.org/projects/microhomie/badge/?version=master
    :target: http://microhomie.readthedocs.io/en/master/?badge=master
    :alt: Documentation Status

.. |pypi| image:: https://img.shields.io/pypi/v/microhomie.svg
    :target: https://pypi.python.org/pypi/microhomie/
    :alt: PyPi Status
