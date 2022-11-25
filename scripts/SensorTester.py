import time
from GpioManager import GpioManager
import RPi.GPIO as GPIO
from threading import Thread


gpioManager = GpioManager()
gpioManager.init()

class SonicThread(Thread):
  def __init__(self , trigger, echo):
    Thread.__init__(self)
    self.trigger = trigger
    self.echo = echo
    self.flag = True

  def run(self):
    while self.flag :
      print(self.measureDistance(self.trigger,self.echo))
      time.sleep(1)

  def measureDistance(self, trigger , echo):

      GPIO.output(trigger, True) # 신호 1 발생
      GPIO.output(trigger, False) # 신호 0 발생(falling 에지)

      while(GPIO.input(echo) == 0):
          pass
      pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
      while(GPIO.input(echo) == 1):
          pass
      pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

      pulse_duration = pulse_end - pulse_start
      return 340*10000/2*pulse_duration

def onOut(time):
  print("감지")

'''
def measureDistance():

    GPIO.output(GpioManager.exitTrigger, True) # 신호 1 발생
    GPIO.output(GpioManager.exitTrigger, False) # 신호 0 발생(falling 에지)

    while(GPIO.input(GpioManager.exitEcho) == 0):
        pass
    pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
    while(GPIO.input(GpioManager.exitEcho) == 1):
        pass
    pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

    pulse_duration = pulse_end - pulse_start
    return 340*10000/2*pulse_duration
'''

def measureDistance(trigger , echo):

    GPIO.output(trigger, True) # 신호 1 발생
    GPIO.output(trigger, False) # 신호 0 발생(falling 에지)

    while(GPIO.input(echo) == 0):
        pass
    pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
    while(GPIO.input(echo) == 1):
        pass
    pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

    pulse_duration = pulse_end - pulse_start
    return 340*10000/2*pulse_duration


def loop(trigger , echo):
  while True:
    print(measureDistance(trigger , echo))

def loop2(trigger,echo):
    while True:
      print(measureDistance(trigger , echo))


#enterSonic = SonicClass.Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onOut)
#exitSonic = SonicClass.Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onOut)


i = input("입력(1,2,3)")

sonic1 = SonicThread(GpioManager.enterTrigger , GpioManager.enterEcho)
sonic2 = SonicThread(GpioManager.exitTrigger , GpioManager.exitEcho)

sonic1.start()

while True:
  pass