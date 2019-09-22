export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

MICROPYVERSION := 1.11
VERSION ?= 2.0.0-beta.3
PORT ?= /dev/ttyUSB0


all: copy-lib firmware

requirements:
	mkdir -p lib/uasyncio
	curl -s -o lib/uasyncio/__init__.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio/uasyncio/__init__.py
	curl -s -o lib/uasyncio/core.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio.core/uasyncio/core.py
	curl -s -o lib/mqtt_as.py https://raw.githubusercontent.com/kevinkk525/micropython-mqtt/master/mqtt_as.py
	curl -s -o lib/asyn.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/asyn.py
	curl -s -o lib/aswitch.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/aswitch.py

copy-lib:
	mkdir -p micropython/ports/esp8266/modules/homie
	cp homie/*.py micropython/ports/esp8266/modules/homie
	cp -rf lib/* micropython/ports/esp8266/modules

firmware:
	cd micropython/ports/esp8266; make

copy-firmware:
	cp micropython/ports/esp8266/build/firmware-combined.bin ./releases/microhomie-esp8266-v$(VERSION).bin

release: all copy-firmware

clean:
	cd micropython/ports/esp8266; make clean
	-rm -rf micropython/ports/esp8266/modules/homie

deploy: erase flash

erase:
	esptool.py --port $(PORT) --baud 460800 erase_flash

flash:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 micropython/ports/esp8266/build/firmware-combined.bin

flash-release:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 releases/microhomie-esp8266-v$(VERSION).bin

espopensdk:
	-git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
	cd esp-open-sdk; make

micropython:
	-git clone --recursive https://github.com/micropython/micropython.git
	cd micropython; git checkout $(MICROPYVERSION)
	cd micropython; make -C mpy-cross
	cd micropython/ports/unix; make axtls; make
	cd micropython; git apply ../micropython.patch

bootstrap: espopensdk micropython requirements


# linting!
black:
	find homie -name '*.py' | grep -v with_errors  | xargs black --line-length=79 --safe $(ARGS)

isort:
	isort --recursive --apply homie

autoflake:
	find homie -name '*.py' | xargs autoflake --in-place --remove-unused-variables

# isort: must come first as black reformats the imports again
# black: must be >19
lint: autoflake isort black
