import os
import datetime
import math

import board
import busio
import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802

os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

# Load cell
loadCelSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

delay = 0.2  # seconds

if not os.path.exists('data_v2'):
    os.makedirs('data_v2')


def getvalues():
    load_Cell = loadCelSensor.read()
    time_of_flight = tofSensor.range
    log_data = load_cell +'%'+ time_of_flight
    return log_data 
