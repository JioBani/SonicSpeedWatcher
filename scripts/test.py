import time
from threading import Thread
class Sonic(Thread):

    def __init__(self):
        Thread.__init__(self)

    def measureDistance(self):
      return 1

    def run(self):
        print("시작")
        i = 0;
        while True:
            i = i + self.measureDistance()
            #print(distance)
            if(i > 1000) : print("넘음")

sonic = Sonic()
sonic.start()

#sonic = NThreadSonic(GpioManager.enterTrigger , GpioManager.enterEcho , onOut)
#sonic.run()

while True:
    pass