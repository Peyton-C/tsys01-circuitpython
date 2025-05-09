#!/usr/bin/python
import tsys01
import board
from time import sleep

i2c = board.I2C
sensor = tsys01.TSYS01(i2c)

while True: # CircuitPython / Modern Style read
    print("temperature %.2f C\t %.2f F") % (sensor.modern_read(), sensor.modern_read(tsys01.UNITS_Farenheit))

while False: # Legacy method from BR
    if not sensor.read():
        print("Error reading sensor")
        exit(1)
    print("Temperature: %.2f C\t%.2f F") % (sensor.temperature(), sensor.temperature(tsys01.UNITS_Farenheit))
    sleep(0.2)