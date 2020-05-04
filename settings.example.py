# Debug mode disables WDT, print mqtt messages
# DEBUG = False

###
# Wifi settings
###

# Name of Wifi
WIFI_SSID = "YOUR_WIFI_SSID"

# Password for the Wifi
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"


###
# MQTT settings
###

# Broker IP or DNS Name
MQTT_BROKER = "10.0.0.1"

# Broker port
# MQTT_PORT = 1883

# Username or None for anonymous login
# MQTT_USERNAME = None

# Password or None for anonymous login
# MQTT_PASSWORD = None

# Defines the mqtt connection timemout in seconds
# MQTT_KEEPALIVE = 30

# SSL connection to the broker. Some MicroPython implementations currently
# have problems with receiving mqtt messages over ssl connections.
# MQTT_SSL = False
# MQTT_SSL_PARAMS = {}
# MQTT_SSL_PARAMS = {"do_handshake": True}

# Base mqtt topic the device publish and subscribes to, without leading slash.
# Base topic format is bytestring.
# MQTT_BASE_TOPIC = "homie"


###
# Device settings
###

# The device ID for registration at the broker. The device id is also the
# base topic of a device and must be unique and bytestring.
# from homie.utils import get_unique_id
# DEVICE_ID = get_unique_id()

# Friendly name of the device as bytestring
# DEVICE_NAME = "mydevice"

# Time in seconds the device updates device properties
# DEVICE_STATS_INTERVAL = 60

# Subscribe to broadcast topic is enabled by default. To disable broadcast
# messages set BROADCAST to False
# BROADCAST = True

# Enable build-in extensions
from homie.constants import EXT_MPY
EXTENSIONS = [EXT_MPY]

# from homie.constants import EXT_MPY, EXT_FW, EXT_STATS
# EXTENSIONS = [
#    EXT_MPY,
#    EXT_FW,
#    EXT_STATS,
# ]
