import time
import SonicClass
from GpioManager import GpioManager

def onOut(time) :
  print("나감 : %f" % time)

# 전역 변수 선언 및 초기화

gpioManager = GpioManager()
gpioManager.init()

startSonic = SonicClass.Sonic(GpioManager.trigger,GpioManager.echo,onOut)
startSonic.triggerDistance = 1000
startSonic.onIn = onIn

while True:
  startSonic.startRun()
  a = input()
  if(a == 'exit') : break
  startSonic.stopRun()
  a = input("재개하려면 아무키나 누르세요.")
  if(a == 'exit') : break