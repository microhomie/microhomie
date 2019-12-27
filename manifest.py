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
        "homie/property.py",
        "homie/utils.py",
        "homie/node/__init__.py",
        "homie/node/base.py",
        "homie/node/micro.py",
    ),
)

# Libs
freeze("./lib", ("mqtt_as.py", "asyn.py", "aswitch.py", "inisetup.py"))

# uasyncio
freeze("./lib", ("uasyncio/__init__.py", "uasyncio/core.py",))
