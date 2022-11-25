import time
import SonicClass
from GpioManager import GpioManager

gpioManager = GpioManager()
gpioManager.init()

def onOut(time):
  print("감지")

enterSonic = SonicClass.Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,onOut)
enterSonic.startRun()