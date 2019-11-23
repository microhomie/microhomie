from micropython import const

# Device
QOS = const(1)
MAIN_DELAY = const(1000)
STATS_DELAY = const(60000)
RESTORE_DELAY = const(250)
WDT_DELAY = const(100)
DEVICE_STATE = b"$state"

# Device states
STATE_INIT = b"init"
STATE_READY = b"ready"
STATE_RECOVER = b"recover"

# Property datatypes
STRING = b"string"
ENUM = b"enum"
BOOLEAN = b"boolean"
INTEGER = b"integer"
FLOAT = b"float"
COLOR = b"color"

# Property formats
RGB = b"rgb"
HSV = b"hsv"

# Node
PUBLISH_DELAY = const(20)

# (Sub)Tobics
T_BC = b"/$broadcast"
T_SET = b"/set"

# General
UTF8 = "utf-8"
SET = b"set"
SLASH = b"/"
UNDERSCORE = b"_"

ON = b"on"
OFF = b"off"
TRUE = b"true"
FALSE = b"false"
LOCKED = b"locked"
UNLOCKED = b"unlocked"
