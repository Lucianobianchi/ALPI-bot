from gpiozero import Button
from time import sleep
import asyncio

button = Button(2)

button.when_pressed = lambda: print('Pressed!')
button.when_released = lambda: print('Stop!')

hola = input("que onda man\n")