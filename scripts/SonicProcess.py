import time
import RPi.GPIO as GPIO
from threading import Thread
from threading import Event
from GpioManager import GpioManager
import multiprocessing as mp

class Sonic():

    def __init__(self ,trigger , echo, triggerDistance , _onOut):
        self.daemon = True
        self.trigger = trigger
        self.echo = echo
        self.triggerDistance = triggerDistance
        self.onOut = _onOut
        self.setRun = False

    def measureDistance(self):

        '''
        물체의 거리를 mm 단위로 반환
        '''

        GPIO.output(self.trigger, True) # 신호 1 발생
        GPIO.output(self.trigger, False) # 신호 0 발생(falling 에지)

        while(GPIO.input(self.echo) == 0):
            pass
        pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
        while(GPIO.input(self.echo) == 1):
            pass
        pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

        pulse_duration = pulse_end - pulse_start
        return 340*10000/2*pulse_duration

    def sonicLoop(self):
        isIn = False
        inTime = 0
        while self.setRun:
            print(distance)
            distance = self.measureDistance()
            if(isIn) :
                if(distance > self.triggerDistance) :
                    outTime =  time.time()
                    noiseStart = time.time()
                    while self.setRun:
                        if(time.time() - noiseStart > 0.1 and distance > self.triggerDistance):
                            transmitTime = outTime - inTime
                            if(transmitTime > 0.01) :
                                self.onOut(transmitTime)
                                isIn = False
                            break

            else:
                if(distance < self.triggerDistance) :
                    isIn = True
                    inTime = time.time()

    def start(self):
      process = mp.Process(name="SubProcess", target=self.sonicLoop)
      process.start()