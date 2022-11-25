import time
from Sonic import Sonic
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
gpioManager.setSonic()

enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onPassEnter)
exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,onPassExit)

enterSonic.start()
enterSonic.start()

while True :
  input("멈추려면 아무키나 눌러주세요")