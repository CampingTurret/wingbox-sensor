# Just in case the environment variables were not properly set
import os
import datetime
import math

os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

import board
import busio
import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802

os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

# Load cell
loadCellSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

delay = 0.5  # seconds

# calibratio data
load_cell_a = 1
load_cell_b = 0
time_of_flight_a = 1
time_of_flight_b = 0

if not os.path.exists('data_v2'):
    os.makedirs('data_v2')

start_time = current_time = datetime.datetime.now()
time_str = start_time.strftime('%Y-%m-%d_%H-%M-%S')
file_str = f'data_v2/test_{time_str}.txt'
delay_datetime = datetime.timedelta(seconds=delay)

with open(file_str, 'w') as f:
    start_message = f'Starting data logging at {start_time.strftime("%H:%M:%S")}:\n'
    f.write(start_message)
    print(start_message[:-2])
    try:
        while True:
            try:
                while current_time + delay_datetime > datetime.datetime.now():
                    pass
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            current_time = datetime.datetime.now()
            # Get sensor readings
            loadCellValue = loadCellSensor.read()
            tofValue = tofSensor.range
            try:
                timestamp = datetime.datetime.now()
                milliseconds = int(float(timestamp.strftime("%f")) / 1000)
                ms_str = str(milliseconds).zfill(3)
                load_cell, time_of_flight = loadCellValue, tofValue
                load_cell_N = float(load_cell) * load_cell_a + load_cell_b
                time_of_flight_cm = float(time_of_flight) * time_of_flight_a + time_of_flight_b
                log_data = f'[{timestamp.strftime("%H:%M:%S")}.{ms_str}]: {load_cell}, {time_of_flight}, ' \
                           f'({load_cell_N} N, {time_of_flight_cm} cm)\n'
            except KeyboardInterrupt:  # unlikely we will catch an interrupt here, but just in case
                raise KeyboardInterrupt
            except (ValueError, TypeError) as e:
                f.write('An error has occurred for the following data point, writing raw data instead\n')
                load_cell, tofValue = loadCellValue, tofValue
                log_data = f'{load_cell}, {tofValue}\n'
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
        f.write(end_message)
        f.write('\n')
        f.write(test_duration_message)
