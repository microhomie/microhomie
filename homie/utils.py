
def get_unique_id():
    try:
        import machine
        return ubinascii.hexlify(machine.unique_id())
    except:
        return "set-a-unique-device-id"

def get_local_ip():
    try:
        import network
        return bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
    except:
        return "127.0.0.1"

def get_local_mac():
    try:
        import network
        return ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
    except:
        return "cannotgetlocalmac"