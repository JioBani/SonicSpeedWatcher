import multiprocessing as mp
import signal
import os
from GpioManager import GpioManager
import time
import RPi.GPIO as GPIO
from MqttClient import *

class Led:
    def __init__(self , led):
        self.led = led
        pass
    def on(self):
        GPIO.output(self.led , 1)

    def off(self):
        GPIO.output(self.led , 0)

GpioManager.init()
GpioManager.setLed()

greenLed = Led(GpioManager.greenLed)
redLed = Led(GpioManager.redLed)

while True:
    a = input("1 : Green , 2 : Red , 3 : Off , 4 : exit")
    if(a == "1") : greenLed.on()
    elif (a == '2') : redLed.on()
    elif (a == '3') :
        greenLed.off()
        redLed.off()
    else : break

