import os
os.environ["BLINKA_MCP2221"] = "1"
os.environ["BLINKA_MCP2221_RESET_DELAY"] = "-1"

from scipy import stats
import time
import board
import busio
import adafruit_vl53l0x
from cedargrove_nau7802 import NAU7802

# Load cell
loadCellSensor = NAU7802(board.I2C(), address=0x2a, active_channels=1)

# Time of flight sensor
i2c = busio.I2C(board.SCL, board.SDA)
tofSensor = adafruit_vl53l0x.VL53L0X(i2c)

# load cell calibration
forces, force_vals = [], []
for i in range(5):
    kgf_input = float(input('Input mass in kg: '))
    forces.append(kgf_input * 9.80665)
    vals_to_average = []
    for j in range(5):
        load_cell = loadCellSensor.read()
        vals_to_average.append(float(load_cell))
        print(f'    Measurement {j + 1}: {load_cell}')
        time.sleep(1)
    force_vals.append(sum(vals_to_average) / len(vals_to_average))
    print(f'Calibration point {i + 1}: force = {forces[i]}, average value = {force_vals[i]}')
    regression = stats.linregress(force_vals, forces)
    print(f'Linear regression for force [N] = a * value + b:\n\ta = {regression.slope}, b = {regression.intercept}')

# time of flight calibration
dists, dist_vals = [], []
for i in range(5):
    dist_input = float(input('Input distance in cm: '))
    dists.append(dist_input)
    vals_to_average = []
    for j in range(5):
        time_of_flight = tofSensor.range
        vals_to_average.append(float(time_of_flight))
        print(f'    Measurement {j + 1}: {time_of_flight}')
        time.sleep(1)
    dist_vals.append(sum(vals_to_average) / len(vals_to_average))
    print(f'Calibration point {i + 1}: distance = {dists[i]}, average value = {dist_vals[i]}')
    regression = stats.linregress(dist_vals, dists)
    print(f'Linear regression for distance [cm] = a * value + b:\n\ta = {regression.slope}, b = {regression.intercept}')
