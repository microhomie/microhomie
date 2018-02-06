
def get_unique_id():
    try:
        import machine
        import ubinascii
        return ubinascii.hexlify(machine.unique_id())
    except:
        return b'set-a-unique-device-id'

def get_local_ip():
    try:
        import network
        return bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
    except:
        return b'127.0.0.1'

def get_local_mac():
    try:
        import network
        import ubinascii
        return ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
    except:
        return b'cannotgetlocalmac'



def wifi_connect(essid, secret):
    """Connects to Wifi"""
    import utime
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        print('NETWORK: connecting to network %s...' % essid)
        wlan.connect(essid, secret)
        while not wlan.isconnected():
            print('NETWORK: waiting for connection...')
            utime.sleep(1)
        print('NETWORK: Connected, network config: %s' % repr(wlan.ifconfig()))

def disable_ap():
    """Disables any Accesspoint"""
    import network
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    print('NETWORK: Access Point disabled.')