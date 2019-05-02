========================
Microhomie relay example
========================

This example uses an array property to address an relay board with more relais. A Microhomie array property is just a HomieNodeProperty with a range > 1. The relay properties in this example are settable, retained and get restored from mqtt retained messages when the device (re-)connect to mqtt.
