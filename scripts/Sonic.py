import time
import RPi.GPIO as GPIO
from threading import Thread
from GpioManager import GpioManager

class Sonic(Thread):

    def __init__(self , trigger, echo, onOut):
        Thread.__init__(self)
        self.daemon = True
        self.trigger = trigger
        self.echo = echo
        self.flag = True
        self.setRun = True
        self.triggerDistance = 1000
        self.onOut = onOut

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

    def run(self):
        while True:
            distance = self.measureDistance()
            print(distance)
            if(distance <self.triggerDistance ) :
                print("넘음")


def onOut(time):
    print("나옴")

gpioManager = GpioManager()
gpioManager.init()
gpioManager.setSonic()

sonic = Sonic(GpioManager.enterTrigger , GpioManager.enterEcho , onOut)

sonic.start()

while True:
    pass