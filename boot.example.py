import gc
import settings
from homie import utils

# Network Setup
utils.disable_ap()
utils.wifi_connect(settings.WIFI_SSID, settings.WIFI_PASSWORD)

# Garbage collection to save up some memory
gc.collect()