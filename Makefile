export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

VERSION := 0.4.0-alpha
MICROPYVERSION := 1.10
PORT := /dev/ttyUSB0


all: copy firmware

requirements:
	mkdir -p micropython/ports/esp8266/modules/uasyncio
	curl -s -o micropython/ports/esp8266/modules/uasyncio/__init__.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio/uasyncio/__init__.py
	curl -s -o micropython/ports/esp8266/modules/uasyncio/core.py https://raw.githubusercontent.com/micropython/micropython-lib/master/uasyncio.core/uasyncio/core.py
	curl -s -o micropython/ports/esp8266/modules/mqtt_as.py https://raw.githubusercontent.com/kevinkk525/micropython-mqtt/master/mqtt_as_minimal.py
	curl -s -o micropython/ports/esp8266/modules/asyn.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/asyn.py
	curl -s -o micropython/ports/esp8266/modules/aswitch.py https://raw.githubusercontent.com/peterhinch/micropython-async/master/aswitch.py

copy:
	mkdir -p micropython/ports/esp8266/modules/homie
	cp homie/*.py micropython/ports/esp8266/modules/homie

firmware:
	cd yaota8266; make
	cd micropython/ports/esp8266; make ota

copy-firmware:
	cp micropython/ports/esp8266/build/firmware-ota.bin ./microhomie-esp8266-ota-v$(VERSION).bin

release: all copy-firmware

clean:
	cd micropython/ports/esp8266; make clean
	-rm -rf micropython/ports/esp8266/modules/homie

deploy: erase flash

erase:
	esptool.py --port $(PORT) --baud 460800 erase_flash

flash:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x0 yaota8266/yaota8266.bin
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0x3c000 micropython/ports/esp8266/build/firmware-ota.bin

espopensdk:
	-git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
	cd esp-open-sdk; make

micropython:
	-git clone --recursive https://github.com/micropython/micropython.git
	cd micropython; git checkout $(MICROPYVERSION)
	cd micropython; make -C mpy-cross
	cd micropython/ports/unix; make axtls; make

yaota:
	-git clone --recursive https://github.com/schinckel/yaota8266.git
	cd yaota8266; git checkout merged
	cd yaota8266; cp config.h.example config.h
	cd yaota8266/ota-client; bash gen_keys.sh
	cd yaota8266/ota-client; python -c "import rsa_sign; rsa_sign.dump_c(rsa_sign.load_key())"

bootstrap: espopensdk micropython requirements yaota
