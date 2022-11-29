import multiprocessing as mp
import signal
import os
from GpioManager import GpioManager
import time
import RPi.GPIO as GPIO

def ledRun(led):
    while True:
        pass

class LedManager:
    def __init__(self):
        greenLed = Led(GpioManager.greenLed , onTime=1)
        redLed =  Led(GpioManager.redLed , onTime=1)
        self.greenLed = greenLed
        self.redLed = redLed
        self.greenLedProcess = mp.Process(name="GreenLed" , target=greenLed.run)
        self.redLedProcess = mp.Process(name="RedLed" , target=redLed.run)

    def start(self):
        self.greenLedProcess.start()
        self.redLedProcess.start()

    def stop(self):
        self.greenLedProcess.kill()
        self.redLedProcess.kill()

    def onGreenLed(self):
        self.greenLed.on()
        pass

    def onRedLed(self):
        self.redLed.off()
        pass

class Led:

    def __init__(self , ledNum , onTime):
        self.isOn = False
        self.isRun = True
        self.start = 0
        self.ledNum = ledNum
        self.onTime = onTime

    def run(self):
        while self.isRun:
            if(self.isOn) :
                if(time.time() - self.startTime > self.onTime) :
                    self.off()

    def on(self):
        self.startTime = time.time()
        self.isOn = True
        GPIO.output(self.ledNum , 1)
        pass

    def off(self):
        GPIO.output(self.ledNum , 0)
        self.isOn = False
        pass

    def loopStop(self):
        self.isRun = False

GpioManager.init()
GpioManager.setLed()
ledManager = LedManager()
ledManager.start()

while True:
    a = input("1 : Green , 2 : Red , 3 : Off , 4 : exit")
    if(a == "1") : ledManager.onGreenLed()
    elif (a == '2') : ledManager.onRedLed()
    else : break