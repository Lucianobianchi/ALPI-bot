try:
    import RPi.GPIO as GPIO
    enviorment = 'raspi'
except (ImportError, RuntimeError):
    try: 
        import Jetson.GPIO as GPIO
        enviorment = 'jetson'
    except (ImportError, RuntimeError):
        from sensors import GPIOMock as GPIO
        enviorment = 'other'

print('Enviorment: ', enviorment)

import time
import threading

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
if enviorment == 'raspi':
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
else: # jetson
    GPIO_TRIGGER = 19
    GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

_distance = -1
is_dead = False

def distance():
    return _distance

def ultrasonic_sensor_thread(name):
    global _distance
    global is_dead

    try: 
        print('Ultrasonic sensor thread')
        while True:
            if is_dead:
                break

            # set Trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
        
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)
        
            start_time = time.time()
            stop_time = time.time()
        
            while GPIO.input(GPIO_ECHO) == 0:
                start_time = time.time()
        
            while GPIO.input(GPIO_ECHO) == 1:
                stop_time = time.time()
        
            # time difference between start and arrival
            time_elapsed = stop_time - start_time
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            _distance = (time_elapsed * 34300) / 2

    finally: 
        GPIO.cleanup()
    

ut = threading.Thread(target=ultrasonic_sensor_thread, args=(1,))

def start():
    ut.start()

def stop():
    global is_dead
    is_dead = True

