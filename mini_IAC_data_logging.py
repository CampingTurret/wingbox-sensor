import os
import math
import serial
import datetime
from IAC_helper import port_scan, development_data

dev = True              # Development mode
usbPort = "editMe"      # Your USB port, obtain using port_scan()

delay = 0.2             # Seconds

try:
    if not dev:
        ser = serial.Serial(usbPort, 9600)
    print("Serial initialized succesfully!")
    running = True
except Exception:
    print("Issue with serial! Aborting...")

def getvalues():
    if dev:
        line = development_data()[:-2].decode('utf-8')
        split_line = line.split(' ')
        load_cell, time_of_flight = split_line[1], split_line[3]
        log_data = load_cell + '%' + time_of_flight
        return log_data
    else:
        line = ser.readline()[:-2].decode('utf-8')
        split_line = line.split(' ')
        load_cell, time_of_flight = split_line[1], split_line[3]
        log_data = load_cell +'%'+ time_of_flight
        return log_data

