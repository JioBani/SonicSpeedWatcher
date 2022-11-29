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
                else:
                    print(time.time() - self.startTime)

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


""" def ledOnOff(led, onOff): # led 번호의 핀에 onOff(0/1) 값 출력하는 함수
        GPIO.output(led, onOff)

onOff = 1
for i in range(10):
        ledOnOff(GpioManager.greenLed, onOff) # led가 연결된  핀에 1또는 0의 디지털 값 출력
        time.sleep(1)
        onOff = 0 if onOff == 1 else 1 # 0과 1의 토글링
 """


ledManager = LedManager()
ledManager.start()

while True:
    a = input("1 : Green , 2 : Red , 3 : Off , 4 : exit")
    if(a == "1") : ledManager.onGreenLed()
    elif (a == '2') : ledManager.onRedLed()
    else : break

