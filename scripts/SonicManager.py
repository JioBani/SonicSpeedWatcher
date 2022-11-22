import time
import RPi.GPIO as GPIO
import SonicClass

n = 0

def onIn() :
  print("들어옴")

def onOut(time) :
  print("%d) 나감 : %f" % n,time)


# 전역 변수 선언 및 초기화
trigger = 24
echo = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, False)

startSonic = SonicClass.Sonic(trigger,echo,onIn,onOut)
startSonic.triggerDistance = 1000
startSonic.startLoop()
startSonic.onIn = onIn