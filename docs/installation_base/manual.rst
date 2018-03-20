Install manually
-----------------

Use your favorite MicroPython remote shell like `rshell <https://github.com/dhylands/rshell>`_, `mpfshell <https://github.com/wendlers/mpfshell>`_ or `ampy <https://github.com/adafruit/ampy>`_ to copy Microhomie to your device.

Create a directory ``homie`` on your device ``lib`` directory and copy the file ``__init__.py`` from the ``homie`` directory. Then create a ``node`` directory in ``homie`` and copy ``__init__.py``, ``led.py``, ``simple.py`` from the ``homie/node`` directory to the device.

Your file system structure should now look similar like this::

    ├── lib
    |   ├── homie
    │   |   ├── __init__.py
    |   │   ├── node
    │   │   |   ├── __init__.py
    │   │   |   ├── led.py
    │   │   |   ├── simple.py
    ├── boot.py
    ├── main.py