import RPi.GPIO as GPIO

class Led:
    def __init__(self , led):
        self.led = led
        pass
    def on(self):
        GPIO.output(self.led , 1)

    def off(self):
        GPIO.output(self.led , 0)