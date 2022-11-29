import SonicManager
from schema.PassData import *
import pickle
from GpioManager import *
import time
import picamera
import multiprocessing as mp
from Led import Led

imagePath = "../static/images/"
imageSendPath = "images/"
speedingStd = 1

greenLed = Led(GpioManager.greenLed)
redLed = Led(GpioManager.redLed)

ledTime = 1
greenLedStart = 0
redLedStart = 0

def getImagePath():
    return "%s%f.jpg" % (imagePath,time.time())

def capture(path):
    camera = picamera.PiCamera()
    camera.capture(path,use_video_port = True)
    camera.close()

def onPass(enterTime, exitTime, passTime, velocity):
    global camera, speedingStd
    if(velocity > speedingStd) : isSpeeding = True
    else : isSpeeding = False
    print("진입 시각 : %f" % enterTime)
    print("진출 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)
    print("과속" if isSpeeding else "정속")

    imageTime = time.time()
    savePath = "%s%f.jpg" % (imagePath,imageTime)
    sendPath = "%s%f.jpg" % (imageSendPath,imageTime)

    path = getImagePath()
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

    with open("../static/data/passData.bin","ab") as file:
        pickle.dump(passData,file)

    if(isSpeeding) :
        redLedStart = time.time()
        redLed.on()
        pass
    else:
        greenLedStart = time.time()
        greenLed.on()
        pass


print("시작")

GpioManager.init()
GpioManager.setSonic()
GpioManager.setLed()
SonicManager.onPass = onPass

SonicManager.run()

try:
    while(True):
        if(time.time() - greenLedStart > ledTime):
            greenLed.off()
        if(time.time() - redLedStart > ledTime):
            redLed.off()
finally:
    greenLed.off()
    redLed.off()
    SonicManager.stop()