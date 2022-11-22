import time
import RPi.GPIO as GPIO
import SonicClass

# 전역 변수 선언 및 초기화
trigger = 24
echo = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, False)

startSonic = SonicClass.Sonic(trigger , echo)

startSonic.sonicLoop()
