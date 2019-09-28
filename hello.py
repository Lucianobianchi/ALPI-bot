#from machine import I2C, Pin
import ssd1306
import time

from smbus2 import SMBus, ic_msg

with SMBus(1) as bus:
    display = ssd1306.SSD1306_I2C(128, 32, bus)

    display.fill(1)  # Fill the entire display with 1="on"
    display.show()
