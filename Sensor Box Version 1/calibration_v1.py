from scipy import stats
import serial
import time

usbPort = 'COM3'

ser = serial.Serial(usbPort, 9000)

# load cell calibration
forces, force_vals = [], []
for i in range(5):
    kgf_input = float(input('Input mass in kg: '))
    forces.append(kgf_input)
    vals_to_average = []
    for j in range(5):
        line = ser.readline()[:-2].decode('utf-8')
        split_line = line.split(' ')
        load_cell = split_line[1]
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
        line = ser.readline()[:-2].decode('utf-8')
        split_line = line.split(' ')
        time_of_flight = split_line[3]
        vals_to_average.append(float(time_of_flight))
        print(f'    Measurement {j + 1}: {time_of_flight}')
        time.sleep(1)
    dist_vals.append(sum(vals_to_average) / len(vals_to_average))
    print(f'Calibration point {i + 1}: distance = {dists[i]}, average value = {dist_vals[i]}')
    regression = stats.linregress(dist_vals, dists)
    print(f'Linear regression for distance [cm] = a * value + b:\n\ta = {regression.slope}, b = {regression.intercept}')
