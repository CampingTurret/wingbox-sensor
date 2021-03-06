# -*- coding: utf-8 -*-
"""
This program is used to load the data from the USB serial.
 Whenever the serial port receives data, it will be placed in
 the "line" variable. From here, it needs to be parsed and saved.
 
You can enable a "development" mode which will feed fake data 
 by setting dev = True
"""

import os
import math
import serial
import datetime
from IAC_helper import port_scan, development_data

dev = False              # Development mode
usbPort = "COM7"      # Your USB port, obtain using port_scan()

delay = 0.02            # Seconds

try:
    if not dev:
        ser = serial.Serial(usbPort, 9600)
    print("Serial initialized succesfully!")
    running = True
except Exception:
    print("Issue with serial! Aborting...")

if not os.path.exists('data'):
    os.makedirs('data')

start_time = current_time = datetime.datetime.now()
time_str = start_time.strftime('%Y-%m-%d_%H-%M-%S')
file_str = 'test.txt'          #i changed the file name!
delay_datetime = datetime.timedelta(seconds=delay)

if dev:
    with open(file_str, 'w') as f:
        try:
            while running:
                try:
                    while current_time + delay_datetime > datetime.datetime.now():
                        pass
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                current_time = datetime.datetime.now()
                try:
                    line = development_data()[:-2].decode('utf-8')
                    timestamp = datetime.datetime.now()
                    milliseconds = int(float(timestamp.strftime("%f")) / 1000)
                    ms_str = str(milliseconds).zfill(3)
                    split_line = line.split(' ')
                    load_cell, time_of_flight = split_line[1], split_line[3]
                    log_data = f'[{timestamp.strftime("%H:%M:%S")}.{ms_str}]: {load_cell},{time_of_flight}\n'
                except KeyboardInterrupt:  # unlikely we will catch an interrupt here, but just in case
                    raise KeyboardInterrupt
                except Exception as e:
                    f.write('An error has occurred for the following data point, writing raw data instead\n')
                    line = development_data()[:-2].decode('utf-8')
                    log_data = line + '\n'
                    print(f'An error has occurred: {e}')
                    print('The following data point will be written as raw data to the file:')
                finally:
                    f.write(log_data)
                    print(log_data[:-2])
        except KeyboardInterrupt:
            end_message = f'Ending logging at {datetime.datetime.now().strftime("%H:%M:%S")}'
            test_duration = (datetime.datetime.now() - start_time) / datetime.timedelta(seconds=1)
            test_duration_mins = math.floor(test_duration / 60)
            test_duration_secs = test_duration % 60
            test_duration_message = f'Test duration: {test_duration_mins} minutes {test_duration_secs:.3f} seconds'
            print(end_message)
            print(test_duration_message)
            

else:
    with open(file_str, 'w') as f:
        try:
            while running:
                try:
                    while current_time + delay_datetime > datetime.datetime.now():
                        pass
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                current_time = datetime.datetime.now()
                try:
                    line = ser.readline()[:-2].decode('utf-8')
                    timestamp = datetime.datetime.now()
                    milliseconds = int(float(timestamp.strftime("%f")) / 1000)
                    ms_str = str(milliseconds).zfill(3)
                    split_line = line.split(' ')
                    load_cell, time_of_flight = split_line[1], split_line[3]
                    log_data = f'[{timestamp.strftime("%H:%M:%S")}.{ms_str}]: {load_cell},{time_of_flight}\n'
                except KeyboardInterrupt:  # unlikely we will catch an interrupt here, but just in case
                    raise KeyboardInterrupt
                except Exception as e:
                    f.write('An error has occurred for the following data point, writing raw data instead\n')
                    line = ser.readline()[:-2].decode('utf-8')
                    log_data = f'{line}\n'
                    print(f'An error has occurred: {e}')
                    print('The following data point will be written as raw data to the file:')
                finally:
                    f.write(log_data)
                    print(log_data[:-2])
        except KeyboardInterrupt:
            end_message = f'Ending logging at {datetime.datetime.now().strftime("%H:%M:%S")}'
            test_duration = (datetime.datetime.now() - start_time) / datetime.timedelta(seconds=1)
            test_duration_mins = math.floor(test_duration / 60)
            test_duration_secs = test_duration % 60
            test_duration_message = f'Test duration: {test_duration_mins} minutes {test_duration_secs:.3f} seconds'
            print(end_message)
            print(test_duration_message)
            
