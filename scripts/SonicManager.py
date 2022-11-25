import time
from Sonic import Sonic
from GpioManager import GpioManager
import os

passTime = 0

def onOut(time) :
  print("나감 : %f" % time)

def onPassEnter(time):
  global passTime
  enterSonic.stop()
  print("입장 시간 : %f" % time)
  passTime = time
  exitSonic.start()

def onPassExit(time):
  exitSonic.stop()
  print("퇴장 시간 : %f" % time)
  print("걸린 시간 : %f" % (time - passTime))
  enterSonic.start()

# 전역 변수 선언 및 초기화

gpioManager = GpioManager()
gpioManager.init()
gpioManager.setSonic()

enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onPassEnter)
exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onPassExit)

enterSonic.start()

while True :
  input("멈추려면 아무키나 눌러주세요")