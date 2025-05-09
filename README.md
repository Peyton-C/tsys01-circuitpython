# tsys01-python
An exprimental CircuitPython module to interface with the TSYS01 temperature sensor. 

## Testing
This library has been tested on:
- Raspberry Pi 4B running Adafruit Blinka & Raspberry Pi OS 12 with a BlueRobotics Temperature Sensor.

# Dependencies
This driver depends on:
- [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)
- [Adafruit Circuitpython BusDevice](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)

# Important Information
- This library will not be rececing any major updates or changes, I do not have access to the hardware anymore.
- Certain functionality of the BlueRobotics Python library are missing or broken.
- The BlueRobotics sensors lack pull-up resistors, which are required for i2C if your MCU/SBC doesn't have its own.
