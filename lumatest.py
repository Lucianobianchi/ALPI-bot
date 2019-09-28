from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import Image, ImageDraw, ImageFont

# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
serial = i2c(port=0, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
device = ssd1306(serial)

with canvas(device) as draw:
    draw.rectangle((10, 10, 130, 130), outline="white", fill="white") 
    
sleep(10)
