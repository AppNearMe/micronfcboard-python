# MicroNFCBoard: Python API
Python API for MicroNFCBoard

![MicroNFCBoard][micronfcboard]

# News

* P2P Support
* Tag writing
* Tag emulation

Support for:

* URI record
* Text record
* Smart poster record
* MIME record

Please update your firmware to use this new version of the Python API.

# License
This code is licensed under the Apache 2.0 License:
http://www.apache.org/licenses/LICENSE-2.0

The USB HID code (in the interface/) directory is from [pyOCD](https://github.com/mbedmicro/pyOCD), licensed under the Apache 2.0 license as well

# Getting started

## Flashing the firmware

Press the ```Bootloader``` button (right) and hold it while inserting the USB cable in your computer. The board should appear as an USB mass storage device with the label ```CRP DISABLD```. If you are upgrading the firmware, you can also hold the ```Bootloader``` button while pressing the ```Reset``` button and then releasing it.

Download the current firmware (version 1.4): http://dev.appnearme.com/static/micronfcboard/fw/firmware-MICRONFCBOARD-d4f6aecb7316.bin

### Windows
Open the ```CRP DISABLD``` drive, erase the ```firmware.bin``` file and drag and drop the firmware file into the disk. Once done, press the ```Reset``` button (left) for a second and release it.

On Windows, you will need to use this file for proper installation of the serial driver:
http://dev.appnearme.com/static/micronfcboard/drivers/micronfcboard_serial.inf

### Mac OS X
Using the terminal, erase the ```firmware.bin``` file from the ```CRP DISABLD``` drive (usually ```/Volumes/CRP\ DISABLD```) and copy the firmware file to the disk. Once done, press the ```Reset``` button (left) for a second and release it.

### Linux
Flashing the firmware using the above methods might not work. If so, use the following command:
```shell
umount /dev/sdX
dd if=firmware-MICRONFCBOARD-*.bin of=/dev/sdX seek=4
```
Replace ```/dev/sdX``` with the correct drive path. Make sure to select the correct drive to avoid losing data!

## Installing the Python dependencies

This Python library should work with any standard Python 2.7 installation.
It relies on a different library for USB transactions, depending on your OS.

Most of them can be installed with a package manager (such as pip).

### Windows
Install [PyWinUSB](https://github.com/rene-aguirre/pywinusb).

### Mac OS X
Install [Cython-HIDAPI](https://github.com/gbishop/cython-hidapi).

### Linux
Install [PyUSB](https://github.com/walac/pyusb). 
A notable dependy is libusb-1.0.

### Running the examples
Navigate to the ```examples/``` directory.

#### Basic
* The ```blink.py``` example will blink the board's LEDs a few times.

#### Tags
* The ```tag_reader.py``` example will poll for tags and display a tag's UID, decoding a NDEF message if available.
* The ```tag_writer.py``` example will poll for tags and display a tag's UID, and then write a NDEF message to the tag.

#### P2P
* The ```p2p_server.py``` example will poll for peers and wait for the peer to push a NDEF message (works with a NFC  phone/tablet or another MicroNFCBoard).
* The ```p2p_client.py``` example will poll for peers and push a NDEF message to the peer (works with a NFC  phone/tablet or another MicroNFCBoard).

#### Tag emulation
* The ```tag_emulator.py``` example will encode a NDEF message, poll for initiators and decode a new NDEF message if written to the emulated tag.

[MicroNFCBoard]: http://appnearme.github.io/micronfcboard/doc/img/micronfcboard-small.png

