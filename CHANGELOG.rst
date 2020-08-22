=========
Changelog
=========

3.0.0-alpha1
------------

* Add support for the new MicroPython uasyncio V3 implementation
* Updated mqtt_as.py version for uasyncio v3
* New uasyncio V3 primitives from Peter Hinch
* Remove update asyncio coroutine. Property data attributes are now published imidiently on change.
* Add available Homie Extensions to constants. Updated ``settings.example.py`` with an example.
* Subscribe to the Homie broadcast topic is now optional and enabled by default.
* The ``utils`` module was refactored to ``homie.network``. This will break ``boot.py`` on update. Replace ``homie.utils`` with ``homie.network`` in ``boot.py`` and other files where you use the ``utils`` module.
* Add validation for datatype integer
* Add the possibility to store multiple WiFi credentials
* Refactored classes

Read Peter's `V3 update guide <https://github.com/peterhinch/micropython-async/blob/master/v3/README.md>`_ to update your coroutines to the new uasyncio v3.


2.3.1
-----

* Fix reset
* Switch to yaota8266 fork from @jedie


2.3.0
-----

* Updated to MicroPython v1.12
* Removed byte / string mix, only strings are allowed
* Experimental MicroPython Homie extension (homie/deviceID/$mpy) to reset the device, start WebREPL and yaota8266 OTA updater (ota version)
* Removed deprecated method HomieDevice.start()
* Start WebREPL if main.py and settings.py are missing or throw an exception (New boot.py)

Breaking changes
~~~~~~~~~~~~~~~~

You may need to update your settings.py and custom nodes and change bytes to strings: In example: b"abcde" to "abcde".


2.2.2
-----

* Bugfix: Do not re-publish data from retained message


2.2.1
-----

* Hotifx: Unsubscribe from retained topic after recover from net/mqtt outage.

2.2.0
-----

* Updated mqqt_as version
* Added debug print method (dprint)
* Fixed runtime error if mqtt broker is not available on first start
* Ignore retained messages on /set sub-topics
* Payload validator
* Message handler (70db1c8)
* Updated documentation

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
