export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

MICROPYVERSION := 1.13
VERSION ?= 3.0.2
PORT ?= /dev/ttyUSB0

export MICROPY_PY_BTREE ?= 0
export MICROPY_VFS_FAT ?= 0
export FROZEN_MANIFEST ?= ../../../manifest.py


all: firmware
ota: firmware-ota

requirements:
	mkdir -p lib

	# Logging module from the standard lib
	curl -s -o lib/logging.py https://raw.githubusercontent.com/micropython/micropython-lib/master/logging/logging.py

	# MQTT async from Kevin Köck
	curl -s -o lib/mqtt_as.py https://raw.githubusercontent.com/kevinkk525/micropython-mqtt/master/mqtt_as.py

	# asyncio v3 primitives from Peter Hinch
	mkdir -p lib/primitives
	curl -s -o lib/primitives/__init__.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/v3/primitives/__init__.py
	curl -s -o lib/primitives/delay_ms.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/v3/primitives/delay_ms.py
	curl -s -o lib/primitives/pushbutton.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/v3/primitives/pushbutton.py
	curl -s -o lib/primitives/message.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/v3/primitives/message.py
	curl -s -o lib/primitives/switch.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/v3/primitives/switch.py

firmware:
	make -C micropython/ports/esp8266 clean-modules
	make -C micropython/ports/esp8266

firmware-ota:
	make -C micropython/ports/esp8266 clean-modules
	make -C micropython/ports/esp8266 ota

copy-firmware:
	cp micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./releases/microhomie-esp8266-v$(VERSION).bin
	cp micropython/ports/esp8266/build-GENERIC/firmware-ota.bin ./releases/microhomie-esp8266-ota-v$(VERSION).bin
	cp micropython/ports/esp8266/build-GENERIC/firmware-ota.bin.ota ./releases/microhomie-esp8266-ota-v$(VERSION).ota

release: clean firmware firmware-ota sign-ota copy-firmware

clean:
	make -C micropython/ports/esp8266 clean

deploy: erase flash

erase:
	esptool.py --port $(PORT) --baud 460800 erase_flash

flash:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 micropython/ports/esp8266/build-GENERIC/firmware-combined.bin

flash-release:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 releases/microhomie-esp8266-v$(VERSION).bin

flash-ota-release:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x3c000 releases/microhomie-esp8266-ota-v$(VERSION).bin

flash-yaota:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 yaota8266/yaota8266.bin

flash-ota:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x3c000 micropython/ports/esp8266/build-GENERIC/firmware-ota.bin

sign-ota:
	yaota8266/cli.py sign micropython/ports/esp8266/build-GENERIC/firmware-ota.bin

espopensdk:
	-git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
	make -C esp-open-sdk

micropython:
	-git clone https://github.com/micropython/micropython.git
	cd micropython; git checkout v$(MICROPYVERSION)
	make -C micropython mpy-cross
	make -C micropython/ports/unix

	make -C micropython/ports/esp8266 submodules
	# cd micropython/ports/esp32; make submodules

yaota:
	-git clone --recursive https://github.com/jedie/yaota8266.git
	cd yaota8266; git checkout develop
	make -C yaota8266 rsa-keys
	cd yaota8266; cp config.h.example config.h

yaota-build:
	make -C yaota8266 build

bootstrap: espopensdk micropython requirements


# linting!
black:
	find homie -name '*.py' | grep -v with_errors | xargs black --line-length=79 --safe $(ARGS)

isort:
	isort --recursive --apply homie

autoflake:
	find homie -name '*.py' | xargs autoflake --in-place --remove-unused-variables

# isort: must come first as black reformats the imports again
# black: must be >19
lint: autoflake isort black
