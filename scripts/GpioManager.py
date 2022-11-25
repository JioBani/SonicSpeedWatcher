import RPi.GPIO as GPIO

class GpioManager:
    enterTrigger = 6
    enterEcho = 5
    exitTrigger = 24
    exitEcho = 23

    def __init__(self) : None

    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.setSonic()

    def setSonic(self):
        GPIO.setup(GpioManager.enterTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.enterEcho, GPIO.IN)
        GPIO.setup(GpioManager.exitTrigger, GPIO.OUT)
        GPIO.setup(GpioManager.exitEcho, GPIO.IN)
        GPIO.output(GpioManager.enterTrigger, False)
        GPIO.output(GpioManager.exitTrigger, False)