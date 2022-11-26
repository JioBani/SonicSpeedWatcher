import time
from Sonic import Sonic
from GpioManager import GpioManager
import os

class SonicManager:
    def __init__(self):
        GpioManager.setSonic()
        self.enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,self.onPassEnter)
        self.exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,self.onPassExit)
        self.enterTime = 0
        self.onPass = None

    def onPassEnter(self,endTime):
        print(self.enterSonic.process)
        if(self.enterSonic.process != None) :
            self.enterSonic.stop()
        print("입장 시간 : %f" % endTime)
        self.enterTime = endTime
        self.exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,self.onPassExit)
        self.exitSonic.start()

    def onPassExit(self,endTime):
        self.exitSonic.stop()
        passTime = endTime - self.enterTime
        kmPerH = 200 / passTime / 1000 * 3.6
        self.onPass(endTime , passTime , kmPerH)
        self.enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,self.onPassEnter)
        self.enterSonic.start()

    def run(self):
        self.enterSonic.start()
        while True :
            input("멈추려면 아무키나 눌러주세요")

    def setOnPass(self , onPass):
        self.onPass = onPass