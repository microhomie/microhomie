import machine
import network
import ubinascii


def disable_ap():
    """Disables any Accesspoint"""
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    print("NETWORK: Access Point disabled.")


def get_unique_id():
    try:
        return ubinascii.hexlify(machine.unique_id())
    except Exception:
        return b"set-a-unique-device-id"


def get_local_ip():
    try:
        return bytes(network.WLAN(0).ifconfig()[0], "utf-8")
    except Exception:
        return b"127.0.0.1"


def get_local_mac():
    try:
        return ubinascii.hexlify(network.WLAN(0).config("mac"), ":")
    except Exception:
        return b"00:00:00:00:00:00"


def reset():
    import machine

    wdt = machine.WDT()
    wdt.feed()
    machine.reset()
