import time
from Sonic import Sonic
from GpioManager import GpioManager
import signal
import multiprocessing as mp
import RPi.GPIO as GPIO

onEnter = None
onExit = None
triggerDistance = 1000
enterTime = 0

def measureDistance(trigger,echo):

    '''
    물체의 거리를 mm 단위로 반환
    '''

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

def enterLoop():
    while True :
        distance = measureDistance(GpioManager.enterTrigger,GpioManager.enterEcho)
        if(distance < triggerDistance) :
            onPassEnter(time.time())
            break

def exitLoop():
    while True :
        distance = measureDistance(GpioManager.exitTrigger,GpioManager.exitEcho)
        if(distance < triggerDistance) :
            onPassExit(time.time())
            break

enterProcess = None
#mp.Process(name="EnterProcess",target=enterLoop)
exitProcess = None
#mp.Process(name="ExitProcess",target=exitLoop)

def onPassEnter(endTime):
    global enterProcess, exitProcess, enterTime
    if(enterProcess != None):
        enterProcess.close()
    print("입장 시간 : %f" % endTime)
    enterTime = time
    exitProcess = mp.Process(name="ExitProcess",target=exitLoop)
    exitProcess.start()

def onPassExit(endTime):
    global enterProcess, exitProcess, enterTime

    print(endTime,enterTime)
    passTime = endTime - enterTime
    kmPerH = 200 / passTime / 1000 * 3.6
    onPass(endTime , passTime , kmPerH)

    exitProcess.close()
    enterProcess = mp.Process(name="EnterProcess",target=enterLoop)
    enterProcess.start()

def onPass(exitTime, passTime, velocity):
    print("퇴장 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)

def run():
    global enterProcess
    enterProcess = mp.Process(name="EnterProcess",target=enterLoop)
    enterProcess.start()
    pass



class SonicManager:
    def __init__(self):
        GpioManager.setSonic()
        self.enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,self.onPassEnter)
        self.exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,self.onPassExit)
        self.enterTime = 0
        self.onPass = None
        self.enterProcess = mp.Process(name="EnterProcess",target=self.enterSonic.sonicSubLoop)
        self.exitProcess = None
        self.isFirst = True

    def onPassEnter(self,endTime) :
        if(self.isFirst == True) :
            self.isFirst = False
        else :
            self.enterProcess.terminate()

        print("입장 시간 : %f" % endTime)
        self.enterTime = endTime
        self.exitProcess = mp.Process(name="ExitProcess",target=self.exitSonic.sonicSubLoop)
        self.exitProcess.start()

#        self.enterSonic.stop()
#        print("입장 시간 : %f" % endTime)
#        self.enterTime = endTime
#       self.exitSonic = Sonic(GpioManager.exitTrigger,GpioManager.exitEcho,1000 ,self.onPassExit)
#        self.exitSonic.start()

    def onPassExit(self,endTime):
        #if(self.exitProcess.is_alive) :
         #   self.exitProcess.terminate()
        passTime = endTime - self.enterTime
        kmPerH = 200 / passTime / 1000 * 3.6
        self.onPass(endTime , passTime , kmPerH)
        self.enterProcess = mp.Process(name="EnterProcess",target=self.enterSonic.sonicSubLoop)
        self.enterProcess.start()

#        self.exitSonic.stop()
#        passTime = endTime - self.enterTime
#        kmPerH = 200 / passTime / 1000 * 3.6
#        self.onPass(endTime , passTime , kmPerH)
#        self.enterSonic = Sonic(GpioManager.enterTrigger,GpioManager.enterEcho, 1000 ,self.onPassEnter)
#        self.enterSonic.start()



    def run(self):
        self.enterProcess.start()
        while True :
            input("멈추려면 아무키나 눌러주세요")

    def setOnPass(self , onPass):
        self.onPass = onPass