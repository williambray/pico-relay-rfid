# app.py
# simple flask app that triggers an output to a rpi pico on GPIO26 to trigger the relay on the pico.
# this does require the use of various adafruit librarys
import board
import digitalio
import time
from flask import Flask

app = Flask(__name__)

# setup output to pico
picoOut = digitalio.DigitalInOut(board.D26)
picoOut.direction = digitalio.Direction.OUTPUT

# Send output to pico to trigger unlock
def triggerUnlock():
    picoOut.value = True
    time.sleep(1)
    picoOut.value = False
    return "Unlocking..."


# Default / Route for reciving the POST request from the Swift App.
@app.route("/", methods=["POST"])
def index_page():
    return triggerUnlock()
