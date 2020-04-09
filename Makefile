export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

MICROPYVERSION := 1.12
VERSION ?= 2.3.1
PORT ?= /dev/ttyUSB0

export MICROPY_PY_BTREE ?= 0
export FROZEN_MANIFEST ?= ../../../manifest.py


all: firmware
ota: firmware-ota

requirements:
	mkdir -p lib/uasyncio
	curl -s -o lib/uasyncio/__init__.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio/uasyncio/__init__.py
	curl -s -o lib/uasyncio/core.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio.core/uasyncio/core.py
	curl -s -o lib/mqtt_as.py https://raw.githubusercontent.com/kevinkk525/micropython-mqtt/21459720051ed33da1358dad9ddfec1a43fa2482/mqtt_as.py
	curl -s -o lib/asyn.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/asyn.py
	curl -s -o lib/aswitch.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/aswitch.py

firmware:
	cd micropython/ports/esp8266; make clean-modules && make

firmware-ota:
	cd micropython/ports/esp8266; make clean-modules && make ota

copy-firmware:
	cp micropython/ports/esp8266/build-GENERIC/firmware-combined.bin ./releases/microhomie-esp8266-v$(VERSION).bin
	cp micropython/ports/esp8266/build-GENERIC/firmware-ota.bin ./releases/microhomie-esp8266-ota-v$(VERSION).bin
	cp micropython/ports/esp8266/build-GENERIC/firmware-ota.bin.ota ./releases/microhomie-esp8266-ota-v$(VERSION).ota

release: clean firmware firmware-ota sign-ota copy-firmware

clean:
	cd micropython/ports/esp8266; make clean

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
	cd esp-open-sdk; make

micropython:
	-git clone --recursive https://github.com/micropython/micropython.git
	cd micropython; git checkout v$(MICROPYVERSION)
	cd micropython; make -C mpy-cross
	cd micropython/ports/unix; make axtls; make
	cd micropython; git apply ../micropython.patch

yaota:
	-git clone --recursive https://github.com/jedie/yaota8266.git
	cd yaota8266; git checkout develop
	cd yaota8266; make rsa-keys;
	cd yaota8266; cp config.h.example config.h

yaota-build:
	cd yaota8266; make build

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
