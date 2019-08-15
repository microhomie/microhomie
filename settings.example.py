from homie.utils import get_unique_id


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
MQTT_BROKER = '10.0.0.1'

# Broker port
MQTT_PORT = 1883

# Username or None for anonymous login
MQTT_USERNAME = None

# Password or None for anonymous login
MQTT_PASSWORD = None

# Defines the mqtt connection timemout in seconds
MQTT_KEEPALIVE = 60

# SSL connection to the broker. Some MicroPython implementations currently
# have problems with receiving mqtt messages over ssl connections.
MQTT_SSL = False
MQTT_SSL_PARAMS = {"do_handshake": True}

# Base mqtt topic the device publish and subscribes to, without leading slash.
# Base topic format is bytestring.
MQTT_BASE_TOPIC = b'homie'


###
# Device settings
###

# The device ID for registration at the broker. The device id is also the
# base topic of a device and must be unique and bytestring.
DEVICE_ID = get_unique_id()

# Friendly name of the device as bytestring
DEVICE_NAME = b'mydevice'

# Time in seconds the device updates device properties
DEVICE_STATS_INTERVAL = 60

# Legacy extensions, for now we only have support for the two legacy extensions.
# Later we will implement the posibility to add extensions.
# No extensions will be loaded per default
EXTENSIONS = []
# EXTENSIONS = [
#     b"org.homie.legacy-firmware:0.1.1:[4.x]",
#     b"org.homie.legacy-stats:0.1.1:[4.x]",
# ]
