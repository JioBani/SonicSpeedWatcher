import RPi.GPIO as GPIO

class GpioManager:
    trigger = 24
    echo = 23

    def __init__(self) : None

    def init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.setSonic()

    def setSonic(self):
        GPIO.setup(GpioManager.trigger, GPIO.OUT)
        GPIO.setup(GpioManager.echo, GPIO.IN)
        GPIO.output(GpioManager.trigger, False)
