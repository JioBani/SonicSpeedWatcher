import time
from GpioManager import GpioManager
import RPi.GPIO as GPIO
from threading import Thread


gpioManager = GpioManager()
gpioManager.init()

def onOut(time):
  print(time)

class SonicThread(Thread):
  def __init__(self , trigger, echo, onOut):
    Thread.__init__(self)
    self.daemon = True
    self.trigger = trigger
    self.echo = echo
    self.flag = True
    self.setRun = True
    self.triggerDistance = 1000
    self.onOut = onOut

  def run(self):
    self.sonicLoop()

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

  def sonicLoop(self):
      isIn = False
      inTime = 0
      while self.setRun:
          distance = self.measureDistance(self.trigger,self.echo)
          print(distance)
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


sonic1 = SonicThread(GpioManager.enterTrigger , GpioManager.enterEcho,onOut)
sonic2 = SonicThread(GpioManager.exitTrigger , GpioManager.exitEcho,onOut)

sonic1.start()
sonic2.start()

while True:
  pass