# code.py
# this script utilizes an RFID relay on pin GP1, a buzzer on GP2, a green led via on GP13, a button input on GP15,
# a relay on GP6 & an input from a raspberry pi both on pin GP26/D26.
# it relies on CircuitPython w/ various adafruit libs which can be seen below.
import board
import busio
import pulseio
import digitalio
import adafruit_ssd1306
import time
import time

# setup the RFID reader
uart = busio.UART(rx=board.GP1, baudrate=9600, bits=8, parity=None, stop=1)
# setup buzzer
buzzer = pulseio.PWMOut(board.GP2, variable_frequency=True)
buzzer.frequency = 440
# setup green led
greenLed = digitalio.DigitalInOut(board.GP13)
greenLed.direction = digitalio.Direction.OUTPUT
# setup button
button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)
# set up relay on pin 6
relay = digitalio.DigitalInOut(board.GP6)
relay.direction = digitalio.Direction.OUTPUT
# setup raspberry pi input
rpiInput = digitalio.DigitalInOut(board.GP26)
rpiInput.switch_to_input(pull=digitalio.Pull.DOWN)

# set up default duty cycles to turn buzzer on and off
BUZZER_OFF = 0
BUZZER_ON = 2 ** 15  # 32768

WIDTH = 128  # oled display width
HEIGHT = 32  # oled display height

# save the values of the key tag and key card
# ADD KEYCARD/KEYTAG VALUES HERE.
keyTag = ""
keyCard = ""

# i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# setup the olde display I2C
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)  # Init oled display

# Clear the oled display in case it has junk on it.
oled.fill(0)

# function handles triggering the relay.
def unlock():
    relay.value = 1
    greenLed.value = True
    oled.text("Unlocking...", 5, 5, True)
    oled.show()
    time.sleep(5)
    relay.value = 0
    oled.fill(0)
    oled.show()
    greenLed.value = False


# Blit the image from the framebuffer to the oled display
while True:
    command = uart.read(12)

    # trigger unlock function if we recieve input from the Raspberry Pi.
    if rpiInput.value:
        print("Recieved input from RPI")
        unlock()

    # trigger unluck function if we recieve input from the button.
    if button.value:
        unlock()

    if command:
        # when a command is detected, sound the buzzer for feedback then check the command recieved.
        oled.fill(0)
        buzzer.duty_cycle = BUZZER_ON
        time.sleep(0.2)
        buzzer.duty_cycle = BUZZER_OFF

        # if the command recieved from the RFID reader matches the keyTag we can trigger the relay
        if command.decode("utf-8") == keyTag:
            unlock()
        else:  # if the command does not match the keyTag show message on oled
            oled.text("Stranger Detected!", 5, 5, True)
            oled.show()
            time.sleep(4)

        command = ""
        oled.fill(0)
        oled.show()
