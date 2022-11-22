import time
import RPi.GPIO as GPIO
import SonicClass

def onIn() :
  print("들어옴")

def onOut() :
  print("나감")

# 전역 변수 선언 및 초기화
trigger = 24
echo = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, False)

startSonic = SonicClass.Sonic(trigger,echo,onIn)
startSonic.triggerDistance = 1000
startSonic.startLoop()
startSonic.onIn = onIn