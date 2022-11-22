class Sonic:

    def __init__(self , _trigger,_echo):
        self.trigger = _trigger
        self.echo = _echo

    def measureDistance(self):

        '''
        물체의 거리를 mm 단위로 반환
        '''

        GPIO.output(self.trigger, True) # 신호 1 발생
        GPIO.output(self.trigger, False) # 신호 0 발생(falling 에지)

        while(GPIO.input(self.echo) == 0):
            pass
        pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
        while(GPIO.input(self.echo) == 1):
            pass
        pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

        pulse_duration = pulse_end - pulse_start
        return 340*1000/2*pulse_duration

    def sonicLoop(self):
        while True:
            distance = self.measureDistance()
            print(distance)