import RPi.GPIO as GPIO

class GpioManager:
    enterTrigger = 6
    enterEcho = 5
    exitTrigger = 24
    exitEcho = 23
    greenLed = 21
    redLed = 20


    def __init__(self) : None

    @staticmethod
    def init():
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @staticmethod
    def setSonic():
        GPIO.setup(GpioManager.enterTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.enterEcho, GPIO.IN)
        GPIO.setup(GpioManager.exitTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.exitEcho, GPIO.IN)
        GPIO.output(GpioManager.enterTrigger, False)
        GPIO.output(GpioManager.exitTrigger, False)

    def setLed():
        GPIO.setup(GpioManager.greenLed, GPIO.OUT)
        GPIO.setup(GpioManager.redLed, GPIO.OUT)