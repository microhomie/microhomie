from mqtt_as import LINUX


if LINUX is False:
    from network import WLAN, AP_IF, STA_IF
    from ubinascii import hexlify


def enable_ap():
    """Disables any Accesspoint"""
    wlan = WLAN(AP_IF)
    wlan.active(True)
    print("NETWORK: Access Point enabled.")


def disable_ap():
    """Disables any Accesspoint"""
    wlan = WLAN(AP_IF)
    wlan.active(False)
    print("NETWORK: Access Point disabled.")


def get_local_ip():
    try:
        return bytes(WLAN(0).ifconfig()[0], "utf-8")
    except NameError:
        return b"127.0.0.1"


def get_local_mac():
    try:
        return hexlify(WLAN(0).config("mac"), ":")
    except NameError:
        return b"00:00:00:00:00:00"


def get_wifi_credentials(wifi):
    wlan = WLAN(STA_IF)
    ssids = wlan.scan()

    for s in ssids:
        ssid = s[0].decode()
        if ssid in wifi:
            return (ssid, wifi[ssid])

    return None
