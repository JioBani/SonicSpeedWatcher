import time
import SonicClass
from GpioManager import GpioManager

def onOut(time) :
  print("나감 : %f" % time)

def onPassEnter(time):
  #exitSonic.startRun()
  print("입장 시간 : %f" % time)
  pass

def onPassExit(time):
  #exitSonic.stopRun()
  print("퇴장 시간 : %f" % time)
  pass

# 전역 변수 선언 및 초기화

gpioManager = GpioManager()
gpioManager.init()

enterSonic = SonicClass.Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onPassEnter)
enterSonic.onOut = onPassEnter

enterSonic.startRun()
while True :
  pass