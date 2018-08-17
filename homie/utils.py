import sys
import utime
import settings
import ubinascii


PYCOM = ('FiPy', 'WiPy', 'LoPy', 'SiPy', 'GPy')

wlan = None
secret = None


def _not_implemented():
    """Generic function for missing network on linux (etc) port"""
    return None


def _setup_network():
    """Setup platform specific network settings"""
    global wlan
    global secret

    if sys.platform in PYCOM:
        # Update secret as tuple with wlan mode for PyCom port.
        wlan = network.WLAN(network.WLAN.STA)
        secret = (network.WLAN.WPA2, settings.WIFI_PASSWORD)
    else:
        # default micropython wlan settings
        wlan = network.WLAN(network.STA_IF)
        secret = settings.WIFI_PASSWORD


def _wifi_connect():
    """Connects to WIFI"""
    if not wlan.isconnected():
        wlan.active(True)
        print('NETWORK: connecting to network %s...' % settings.WIFI_SSID)
        wlan.connect(settings.WIFI_SSID, secret)
        while not wlan.isconnected():
            print('NETWORK: waiting for connection...')
            utime.sleep(1)
        print('NETWORK: Connected, network config: %s' % repr(wlan.ifconfig()))


# Only import network and machine if we run on a device and map the
# functions. Ports like the linux port have no such libraries.
if sys.platform not in ('linux'):
    import machine
    import network
    setup_network = _setup_network
    wifi_connect = _wifi_connect
else:
    setup_network = _not_implemented
    wifi_connect = _not_implemented


def disable_ap():
    """Disables any Accesspoint"""
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    print('NETWORK: Access Point disabled.')


def get_unique_id():
    try:
        return ubinascii.hexlify(machine.unique_id())
    except Exception:
        return b'set-a-unique-device-id'


def get_local_ip():
    try:
        return bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
    except Exception:
        return b'127.0.0.1'


def get_local_mac():
    try:
        return ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
    except Exception:
        return b'cannotgetlocalmac'
