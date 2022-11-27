import SonicManager
from schema.PassData import *
import pickle
from GpioManager import *
import time
import picamera
import multiprocessing as mp

imagePath = "../static/images/"
speedingStd = 1

def getImagePath():
    global imagePath
    return "%s%f.jpg" % (imagePath,time.time())

def capture(path):
    camera = picamera.PiCamera()
    camera.capture(path,use_video_port = True)
    camera.close()

def onPass(exitTime, passTime, velocity):
    global camera, speedingStd
    if(velocity > speedingStd) : isSpeeding = True
    else : isSpeeding = False
    print("퇴장 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)
    print("과속" if isSpeeding else "정속")

    path = getImagePath()
    cameraProcess = mp.Process(target=capture,args=(path,))
    cameraProcess.start()
    cameraProcess.join()

    passData = PassData(
        exitTime=exitTime,
        passingTime=passTime,
        velocity=velocity,
        imagePath=path,
        isSpeeding=isSpeeding
    )

    with open("../static/data/passData.bin","ab") as file:
        pickle.dump(passData,file)


print("시작")

GpioManager.init()
GpioManager.setSonic()
SonicManager.onPass = onPass

SonicManager.run()

input("종료하려면 아무 키나 입력")
SonicManager.stop()
