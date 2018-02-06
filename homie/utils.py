import sys
import utime
import settings
import ubinascii

# Only import network and machine if we run on a device. Ports like
# the linux port have no such libraries.
if sys.platform not in ('linux'):
    import machine
    import network


PYCOM = ('FiPy', 'WiPy', 'LoPy', 'SiPy', 'GPy')

secret = None
wlan = None

# Platform specific network settings
if sys.platform in PYCOM:
    # Update secret as tuple with wlan mode for PyCom port.
    wlan = network.WLAN(network.WLAN.STA)
    secret = (network.WLAN.WPA2, secret)
else:
    # default micropython wlan settings
    wlan = network.WLAN(network.STA_IF)
    secret = settings.WIFI_PASSWORD


def wifi_connect():
    """Connects to Wifi"""
    if not wlan.isconnected():
        wlan.active(True)
        print('NETWORK: connecting to network %s...' % settings.WIFI_SSID)
        wlan.connect(settings.WIFI_SSID, secret)
        while not wlan.isconnected():
            print('NETWORK: waiting for connection...')
            utime.sleep(1)
        print('NETWORK: Connected, network config: %s' % repr(wlan.ifconfig()))


def disable_ap():
    """Disables any Accesspoint"""
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    print('NETWORK: Access Point disabled.')


def get_unique_id():
    try:
        return ubinascii.hexlify(machine.unique_id())
    except:
        return b'set-a-unique-device-id'


def get_local_ip():
    try:
        return bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
    except:
        return b'127.0.0.1'


def get_local_mac():
    try:
        return ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
    except:
        return b'cannotgetlocalmac'
