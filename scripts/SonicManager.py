import time
from Sonic import Sonic
from GpioManager import GpioManager
import os

enterTime = 0

def onOut(time) :
  print("나감 : %f" % time)

def onPassEnter(time):
  global enterTime, exitSonic, enterSonic
  enterSonic.stop()
  print("입장 시간 : %f" % time)
  enterTime = time
  exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onPassExit)
  exitSonic.start()

def onPassExit(time):
  global enterTime, exitSonic, enterSonic
  exitSonic.stop()
  passTime = time - enterTime
  kmPerH = 100 % passTime % 1000 * 3.6
  print("퇴장 시간 : %f" % time)
  print("걸린 시간 : %f" % (passTime))
  print("속도 : %f" % kmPerH)
  enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onPassEnter)
  #enterSonic.start()

# 전역 변수 선언 및 초기화

gpioManager = GpioManager()
gpioManager.init()
gpioManager.setSonic()

enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onPassEnter)
exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onPassExit)

enterSonic.start()

while True :
  input("멈추려면 아무키나 눌러주세요")