import time
from GpioManager import GpioManager
import multiprocessing as mp
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

onEnter = None
onExit = None
onPass = None
triggerDistance = 1000 #. 차량이 지나가고 있다고 감지할 거리 (10cm)
enterTime = 0
overSpeedStd = 1.5 #. 과속 기준

#. 거리 측정
def measureDistance(trigger,echo):

    '''
    물체의 거리를 mm 단위로 반환
    '''

    GPIO.output(trigger, True) # 신호 1 발생
    GPIO.output(trigger, False) # 신호 0 발생(falling 에지)

    while(GPIO.input(echo) == 0):
        pass
    pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
    while(GPIO.input(echo) == 1):
        pass
    pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

    pulse_duration = pulse_end - pulse_start
    return 340*10000/2*pulse_duration

#. 입구 초음파 센서에서 차량 감지
def enterLoop():
    while True :
        distance = measureDistance(GpioManager.enterTrigger,GpioManager.enterEcho)
        if(distance < triggerDistance) :
            onPassEnter(time.time()) #. 감지한 경우 onPassEnter 실행
            break

#. 출구 초음파 센서에서 차량 감지
def exitLoop():
    #. matt 객체 생성
    client = mqtt.Client()
    client.connect('localhost', 1883)
    client.loop_start()
    while True :
        distance = measureDistance(GpioManager.exitTrigger,GpioManager.exitEcho)
        if(distance < triggerDistance) :
            onPassExit(time.time() , client) #. 감지한 경우 onPassExit 실행
            break
    client.loop_stop()

enterProcess = None
exitProcess = None

#. 차량이 입구 초음파에 감지되었을때
def onPassEnter(checkTime):
    global enterProcess, exitProcess, enterTime

    #. 입구 초음파 작동 중지
    if(enterProcess != None):
        enterProcess.close()
    print("입장 시간 : %f" % checkTime)

    #. 진입 시각을 기록(checkTime : 감지된 시각)
    enterTime = checkTime

    #. 출구 초음파 센서 감지 프로세스 시작
    exitProcess = mp.Process(name="ExitProcess",target=exitLoop)
    exitProcess.start()

#. 차량이 출구 초음파에 감지되었을때
def onPassExit(endTime , client):
    global enterProcess, exitProcess, enterTime

    passTime = endTime - enterTime #. 통과하는데 걸린 시간 계산
    kmPerH = 200 / passTime / 1000 * 3.6 #. 평균 속도 계산

    #. 과속 판별
    if(kmPerH > overSpeedStd) :
        client.publish('velocity' , str(kmPerH) + '/과속')
    else :
        client.publish('velocity' , str(kmPerH) + '/정속')

    #. SystemManager의 콜백 실행
    onPass(enterTime, endTime , passTime , kmPerH)

    #. 출구 초음파 종료
    exitProcess.close()

    #. 입구 초음파 실행
    enterProcess = mp.Process(name="EnterProcess",target=enterLoop)
    enterProcess.start()


#. SonicManager 시작
def run():
    global enterProcess
    enterProcess = mp.Process(name="EnterProcess",target=enterLoop)
    enterProcess.start()

#. SonicManager 정지
def stop():
    if(enterProcess.is_alive) : enterProcess.kill()
    if(exitProcess.is_alive) : enterProcess.kill()