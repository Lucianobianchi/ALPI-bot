from gpiozero import Button
from time import sleep
import asyncio

RED_BUTTON = Button(2)
BLUE_BUTTON = Button(3)

RED_BUTTON.when_pressed = lambda: print('RED Pressed!')
RED_BUTTON.when_released = lambda: print('RED Stop!')

BLUE_BUTTON.when_pressed = lambda: print('BLUE Pressed!')
BLUE_BUTTON.when_released = lambda: print('BLUE Stop!')

hola = input("que onda man\n")