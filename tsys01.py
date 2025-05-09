from board import *
import sys
from adafruit_bus_device.i2c_device import I2CDevice
    
import time

try: # This was in the library i was using for refrence.
    import typing  # pylint: disable=unused-import
    from typing_extensions import Literal
    from busio import I2C
except ImportError:
    pass

# Valid units
UNITS_Centigrade = 1
UNITS_Farenheit  = 2
UNITS_Kelvin     = 3
    
class TSYS01(object):
    
    # Registers
    _TSYS01_ADDR        = 0x77
    _TSYS01_PROM_READ   = 0xA0
    _TSYS01_RESET       = 0x1E
    _TSYS01_CONVERT     = 0x48
    _TSYS01_READ        = 0x00
    
    def _read_word(self, register): # Circuitpython's bus device doesn't have an equivilant to smbus2's read_word_data
        result = bytearray(2)
        #self._i2c_device.write_then_readinto(bytes({register}), result)
        self._i2c_device.write_then_readinto(bytes([register]), result)
        return int.from_bytes(result, 'big')

    def __init__(self, i2c_bus):
        self._i2c_device = I2CDevice(i2c_bus, self._TSYS01_ADDR)

        # Degrees C
        self._temperature = 0
        self._k = []

        with self._i2c_device:
            self._i2c_device.write(bytes([self._TSYS01_RESET]))
            time.sleep(0.1)

            # Read calibration values
            # Read one 16 bit byte word at a time
            for prom in range(0xAA, 0xA2-2, -2):
                k = self._read_word(prom)
                self._k.append(k)
            '''for prom in range(0xA0, 0xAE + 2, 2):
                k = self._read_word(prom)
                self._k.append(k)'''
            
            if len(self._k) < 5:
                raise RuntimeError("Reading failed!!")
            #self._k.reverse() #Use in case if readings are wrong!
    
    def read(self):
        # Request conversion
        self._i2c_device.write(bytes([self._TSYS01_CONVERT]))
    
        # Max conversion time = 9.04 ms
        time.sleep(0.01)

        adc = bytearray(3)
        #self._i2c_device.write(bytes([self._TSYS01_READ]))
        #self._i2c_device.readinto(adc)
        self._i2c_device.write_then_readinto(bytes([self._TSYS01_READ]), adc)
        
        adc = adc[0] << 16 | adc[1] << 8 | adc[2]
        self._calculate(adc)
        return True

    # Temperature in requested units
    # default degrees C
    def temperature(self, conversion=UNITS_Centigrade):
        if conversion == UNITS_Farenheit:
            return (9/5) * self._temperature + 32
        elif conversion == UNITS_Kelvin:
            return self._temperature + 273
        return self._temperature

    # Cribbed from datasheet
    def _calculate(self, adc):
        adc16 = adc/256
        self._temperature = -2 * self._k[4] * 10**-21 * adc16**4 + \
            4  * self._k[3] * 10**-16 * adc16**3 +                \
            -2 * self._k[2] * 10**-11 * adc16**2 +                \
            1  * self._k[1] * 10**-6  * adc16   +                 \
            -1.5 * self._k[0] * 10**-2
    
    def modern_read(self, conversion=UNITS_Centigrade): # Fits closer with how most circuitpython libraries handle reading
        if not self.read():
            print("Failed to read from sensor")
            exit(1)
        return self.temperature(conversion)