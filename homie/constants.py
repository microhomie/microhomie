from micropython import const

# Device
QOS = const(1)
MAIN_DELAY = const(1000)
STATS_DELAY = const(60000)
WDT_DELAY = const(100)
DEVICE_STATE = "$state"

# Device states
STATE_INIT = "init"
STATE_READY = "ready"
STATE_RECOVER = "recover"

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

# Node
PUBLISH_DELAY = const(20)

# (Sub)Tobics
T_BC = "/$broadcast"
T_SET = "/set"

# General
UTF8 = "utf-8"
SET = "set"
SLASH = "/"
UNDERSCORE = b"_"

ON = "on"
OFF = "off"
TRUE = "true"
FALSE = "false"
LOCKED = "locked"
UNLOCKED = "unlocked"
