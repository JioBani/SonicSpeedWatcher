from SonicManager import *

def onPass(exitTime, passTime, velocity):
  print("퇴장 시각 : %f" % exitTime)
  print("통과 시간 : %f" % passTime)
  print("평균 속도 : %f" % velocity)

GpioManager.init()

sonicManager = SonicManager()
sonicManager.setOnPass(onPass=onPass)
sonicManager.run()