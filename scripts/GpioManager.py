import RPi.GPIO as GPIO

#. Gpio를 관리하기 위한 class
class GpioManager:

    #. GPIO 핀 번호 지정
    enterTrigger = 6 #. 입구 초음파 trig
    enterEcho = 5 #. 입구 초음파 echo
    exitTrigger = 24 #. 출구 초음파 trig
    exitEcho = 23 #. 출구 초음파 echo
    greenLed = 21 #. 초록색 Led
    redLed = 20 #. 빨간색 Led


    def __init__(self) : None

    #. Gpio 시작 설정
    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    #. 초음파 센서 핀 입출력 설정
    @staticmethod
    def setSonic():
        GPIO.setup(GpioManager.enterTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.enterEcho, GPIO.IN)
        GPIO.setup(GpioManager.exitTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.exitEcho, GPIO.IN)
        GPIO.output(GpioManager.enterTrigger, False)
        GPIO.output(GpioManager.exitTrigger, False)

    #. led 핁 입출력 설정
    def setLed():
        GPIO.setup(GpioManager.greenLed, GPIO.OUT)
        GPIO.setup(GpioManager.redLed, GPIO.OUT)