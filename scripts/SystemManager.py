import SonicManager
from schema.PassData import *
import pickle
from GpioManager import *
import time
import picamera
import multiprocessing as mp
from Led import Led
from MqttClient import MqttClient
from DataManager import DataManager
from PIL import Image


processManager = mp.Manager() #. 프로세스 관리를 위한 객체
dataManager = DataManager() #. 데이터 입출력을 위한 객체

imagePath = "../static/images/"
imageSendPath = "images/"
speedingStd = 1.5 #. 과속 기준(1.5km)
ledTime = 2 #. led가 켜지는 시간(2초)

greenLed = Led(GpioManager.greenLed)
redLed = Led(GpioManager.redLed)

#. 멀티 프로세스에서 값을 동기화 하기 위한 작업
#. led의 시작 시간 변수 선언
greenLedStart = processManager.Value(typecode='d' , value=0)
redLedStart = processManager.Value(typecode='d' , value=0)

#. mqtt에서 데이터를 달라는 메세지를 받았을때
def onMessage(client, userdata, msg):
  content = str(msg.payload.decode("utf-8"))
  print(content)
  #. 데이터를 읽어서 "json_response" 토픽으로 송신
  if(content == 'request'):
        message = dataManager.readByJson()
        mqttClient.publish("json_response", message)
        print("sending %s" % message)

#.mqtt 통신
mqttClient = MqttClient(ip="localhost" , topic="json_request" ,onMessage=onMessage)
mqttClient.run()


#. 저장할 이미지의 경로 반환
def getImagePath():
    return "%s%f.jpg" % (imagePath,time.time())

#. pi camera로 사진 촬영
def capture(path):
    camera = picamera.PiCamera()
    camera.capture(path,use_video_port = True)
    camera.close()

#. SonicManager에서 차량이 단속 구간을 통과했을때 실행될 콜백
def onPass(enterTime, exitTime, passTime, velocity):
    global camera, speedingStd

    #. 과속인지 판별
    if(velocity > speedingStd) : isSpeeding = True
    else : isSpeeding = False

    print("진입 시각 : %f" % enterTime)
    print("진출 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)
    print("과속" if isSpeeding else "정속")

    #. 현재 시각으로 이미지 이름을 만듬
    #. 앱에서 저장할때와 웹에서 접근할때 경로가 다르기 때문에 따로 적용
    imageTime = time.time()
    savePath = "%s%f.jpg" % (imagePath,imageTime)
    sendPath = "%s%f.jpg" % (imageSendPath,imageTime)

    #path = getImagePath()
    #. 사진 촬영 실행
    cameraProcess = mp.Process(target=capture,args=(savePath,))
    cameraProcess.start()
    cameraProcess.join()

    passData = PassData(
        enterTime=enterTime,
        exitTime=exitTime,
        passingTime=passTime,
        velocity=velocity,
        imagePath=sendPath,
        isSpeeding=isSpeeding
    )

    try:
        if(not isSpeeding) :
            greenLedStart.value = time.time()
            greenLed.on()
        else:
            redLedStart.value = time.time()
            redLed.on()
    except Exception:
        import traceback
        traceback.print_exc()

    with open("../static/data/passData.bin","ab") as file:
        pickle.dump(passData,file)

    image = Image.open(savePath)
    image = image.rotate(90)
    image.save(savePath)



print("시작")

GpioManager.init()
GpioManager.setSonic()
GpioManager.setLed()

SonicManager.onPass = onPass
SonicManager.run()

try:
    while True :
        if(time.time() - greenLedStart.value > ledTime) :
            greenLed.off()
        if(time.time() - redLedStart.value > ledTime) :
            redLed.off()
        time.sleep(0.1)
finally:
    greenLed.off()
    redLed.off()
    SonicManager.stop()
    mqttClient.stop()