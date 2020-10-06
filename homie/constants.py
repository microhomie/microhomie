from micropython import const

# Device
QOS = const(1)
MAIN_DELAY = const(1000)
STATS_DELAY = const(60000)
WDT_DELAY = const(100)

# Device states
STATE_INIT = "init"
STATE_READY = "ready"
STATE_RECOVER = "recover"
STATE_OTA = "ota"
STATE_WEBREPL = "webrepl"

# Property datatypes
STRING = "string"
ENUM = "enum"
BOOLEAN = "boolean"
INTEGER = "integer"
FLOAT = "float"
COLOR = "color"

# Property formats
RGB = "rgb"
HSV = "hsv"

# (Sub)Topics
DEVICE_STATE = "$state"
T_BC = "$broadcast"
T_MPY = "$mpy"
T_SET = "/set"

# General
UTF8 = "utf-8"
SET = "set"
SLASH = "/"
UNDERSCORE = "_"

ON = "on"
OFF = "off"
TRUE = "true"
FALSE = "false"
LOCKED = "locked"
UNLOCKED = "unlocked"

# Build-in extension strings
EXT_MPY = "org.microhomie.mpy:0.1.0:[4.x]"
EXT_FW = "org.homie.legacy-firmware:0.1.1:[4.x]"
EXT_STATS = "org.homie.legacy-stats:0.1.1:[4.x]"
