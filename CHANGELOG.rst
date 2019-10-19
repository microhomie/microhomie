=========
Changelog
=========

2.1.0
-----

* Add DEBUG setting to disable WDT
* Update mqtt_as, improves connection integrity at cost of power consumption (ESP8266)
* Add Linux support
* Add more datatypes to constants
* Update mqtt_as (close socket if first connection fails/wrong)

Refactor subscribtions:

* Settable and not settable propterties can now restore from a topic with retained payload
* Unsubscribe from restore topics after device properties are published and before asyncio coros start to publish node data

2.0.0
-----

* Update to Homie v4
* Remove code for arrays
* Add legacy extensions, default disabled

1.0.0
-----

* Release version 1.0.0
* Update docs for ESP32


1.0.0-beta2
-----------

* Update to MicroPython 1.11
* Reset device if can not connect to mqtt on first start


1.0.0-beta1
-----------

* Add mpfshell install script and documentation for ESP32 boards.
* Download requirements to lib/ directory


1.0.0-alpha3
------------

* Fix restore from array property
* Add One-Wire example node for ds18b20 (Thanks Rick @palmtreefrb)


1.0.0-alpha2
------------

* Add level to broadcast messages
* Fix property.data send updates when set
* Rename msg to payload in examples


1.0.0-alpha
-----------

This version is not compatible with the previous 0.3 version.

* Switch to asyncio and use mqtt_as from Peter Hinch, with the PR from Kevin Köck
* Add node proptery class
* Automate publishing node properties
* Refactored a lot of methods
* Add contanst
* Mount device class to node class on add_node()
* Updated example nodes
* Included asyn, aswitch from Peter Hinch
* Pre-Build images, Microhomie with asyncio is to big to run from flash drive or install via upip
