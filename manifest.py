# WebREPL
freeze("$(MPY_DIR)/extmod/webrepl", ("webrepl.py", "websocket_helper.py",))

# Modules
freeze('$(PORT_DIR)/modules')

# Tools
freeze('$(MPY_DIR)/tools', ('upip.py', 'upip_utarfile.py'))

# drivers
freeze('$(MPY_DIR)/drivers/dht', 'dht.py')
freeze('$(MPY_DIR)/drivers/onewire')

# Microhomie
include
freeze(".", "homie/__init__.py")
freeze(".", "homie/constants.py")
freeze(".", "homie/device.py")
freeze(".", "homie/micro.py")
freeze(".", "homie/node.py")
freeze(".", "homie/property.py")
freeze(".", "homie/utils.py")

# Libs
freeze("./lib", ("mqtt_as.py", "asyn.py", "aswitch.py",))

# uasyncio
freeze("./lib", "uasyncio/__init__.py")
freeze("./lib", "uasyncio/core.py")
