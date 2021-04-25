# Pico Relay RFID Pico code

This is the code for the Pico microcontroller as part of the Pico Relay RFID project. This script utilizes an RFID relay on pin GP1, a buzzer on GP2, a green led via on GP13, a button input on GP15, a relay on GP6 & an input from a raspberry pi both on pin GP26/D26.

It relies on CircuitPython w/ various adafruit libs are included in the repository.

## Usage

First you will need to load the adafruit circuitpython UF2 file onto the Pico.

1. Hold the BOOTSEL button on the pico while plugging the pico into your computer.
1. Find the Pico in your mounted drives and copy the file `adafruit-circuitpython-raspberry_pi_pico-en_GB-6.2.0.uf2` to the root of the pico.
1. The pico should restart then remount to the device and be called `CIRCUITPY`.

Once the new UF2 on the Pico you can copy the following files to the Pico:

- `code.py`
- `/lib`
- `font5x8.bin`

The pico should safe reboot after adding all the files and will begin running the code.
