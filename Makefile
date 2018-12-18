export PATH := $(PWD)/esp-open-sdk/xtensa-lx106-elf/bin:$(PWD)/micropython/tools:$(PWD)/micropython/ports/unix:$(HOME)/go/bin:$(PATH)

VERSION := 0.3.1
MICROPYVERSION := 1.9.4
PORT := /dev/ttyUSB0


all: clean copy firmware

requirements:
	micropython -m upip install -p micropython/ports/esp8266/modules micropython-umqtt.simple

copy:
	mkdir -p micropython/ports/esp8266/modules/homie/node
	cp homie/*.py micropython/ports/esp8266/modules/homie
	cp homie/node/__init__.py micropython/ports/esp8266/modules/homie/node

firmware:
	cd micropython/ports/esp8266; make

copy-firmware:
	cp micropython/ports/esp8266/build/firmware-combined.bin ./microhomie-esp8266-v$(VERSION).bin

release: all copy-firmware

clean:
	cd micropython/ports/esp8266; make clean
	-rm -rf micropython/ports/esp8266/modules/homie

deploy: erase flash

erase:
	esptool.py --port $(PORT) --baud 460800 erase_flash

flash:
	esptool.py --port $(PORT) --baud 460800 write_flash  --flash_size=detect --verify -fm dio 0 micropython/ports/esp8266/build/firmware-combined.bin

espopensdk:
	-git clone --recursive https://github.com/pfalcon/esp-open-sdk.git
	cd esp-open-sdk; make

micropython:
	-git clone --recursive https://github.com/micropython/micropython.git
	cd micropython; git checkout -b $(MICROPYVERSION)
	cd micropython; make -C mpy-cross
	cd micropython/ports/unix; make axtls; make

bootstrap: espopensdk micropython requirements
