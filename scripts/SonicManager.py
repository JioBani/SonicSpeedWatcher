import time
import SonicClass
from GpioManager import GpioManager

def onIn() :
  print("들어옴")

def onOut(time) :
  print("나감 : %f" % time)


# 전역 변수 선언 및 초기화

gpioManager = GpioManager()
gpioManager.init()

startSonic = SonicClass.Sonic(onIn,onOut)
startSonic.triggerDistance = 1000
startSonic.startLoop()
startSonic.onIn = onIn