import time
import SonicClass
from GpioManager import GpioManager
import RPi.GPIO as GPIO

gpioManager = GpioManager()
gpioManager.init()

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


#enterSonic = SonicClass.Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onOut)
#exitSonic = SonicClass.Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onOut)

while True:
  print(measureDistance(GpioManager.enterTrigger , GpioManager.enterEcho))
  print(measureDistance(GpioManager.exitTrigger ,GpioManager.exitEcho ))
  time.sleep(1)