# WebREPL
freeze("$(MPY_DIR)/extmod/webrepl", ("webrepl.py", "websocket_helper.py",))

# Modules
freeze(
    "$(PORT_DIR)/modules",
    (
        "_boot.py",
        "apa102.py",
        "flashbdev.py",
        "neopixel.py",
        "ntptime.py",
        "port_diag.py",
    ),
)

# Tools
freeze("$(MPY_DIR)/tools", ("upip.py", "upip_utarfile.py"))

# drivers
freeze("$(MPY_DIR)/drivers/dht", "dht.py")
freeze("$(MPY_DIR)/drivers/onewire")

# Microhomie
freeze(
    ".",
    (
        "homie/__init__.py",
        "homie/constants.py",
        "homie/device.py",
        "homie/node.py",
        "homie/property.py",
        "homie/network.py",
        "homie/validator.py",
    ),
)

# Libs
freeze("./lib", (
    "inisetup.py",
    "logging.py",
    "mqtt_as.py",
    "primitives/__init__.py",
    "primitives/delay_ms.py",
    "primitives/message.py",
    "primitives/pushbutton.py",
    "primitives/switch.py",
    )
)

# uasyncio
include("$(MPY_DIR)/extmod/uasyncio/manifest.py")
