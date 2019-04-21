from micropython import const

# Device
QOS = const(1)
MAIN_DELAY = const(5000)
STATS_DELAY = const(60000)
RESTORE_DELAY = const(250)
DEVICE_STATE = b"$state"

# Node
PUBLISH_DELAY = const(25)

# General
SLASH = b"/"

ON = b"on"
OFF = b"off"
TRUE = b"true"
FALSE = b"false"
LOCKED = b"locked"
UNLOCKED = b"unlocked"
