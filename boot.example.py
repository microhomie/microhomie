import gc
import utime
import network

def wifi_connect(essid, secret):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network %s...' % essid)
        wlan.connect(essid, secret)
        while not wlan.isconnected():
            print('waiting for connection...')
            utime.sleep(1)
        print('Connected, network config: %s' % repr(wlan.ifconfig()))

def disable_ap():
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    print('Access Point disabled.')

disable_ap()

wifi_connect('YOUR_WIFI_SSID', 'YOUR_WIFI_PASSWORD')   # CHANGE THIS!

# import webrepl
# webrepl.start()
gc.collect()