from micropython import const

# Device
QOS = const(1)
MAIN_DELAY = const(1000)
STATS_DELAY = const(60000)
RESTORE_DELAY = const(250)
DEVICE_STATE = b"$state"

# Node
PUBLISH_DELAY = const(20)

# General
SLASH = b"/"
UNDERSCORE = b"_"

ON = b"on"
OFF = b"off"
TRUE = b"true"
FALSE = b"false"
LOCKED = b"locked"
UNLOCKED = b"unlocked"
