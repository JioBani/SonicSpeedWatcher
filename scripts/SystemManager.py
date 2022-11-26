import SonicManager
from schema.PassData import *
import pickle
from GpioManager import *
import time
import picamera

imagePath = "../static/images"

def getImagePath():
    global imagePath
    return "%f%d.jpg" % (time.time() ,imagePath )

def onPass(exitTime, passTime, velocity):
    print("퇴장 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)

    path = getImagePath()

    with picamera.PiCamera() as camera:
        camera.capture(path)

    passData = PassData(
        exitTime=exitTime,
        passingTime=passTime,
        velocity=velocity,
        imagePath=path
    )

    with open("../static/data/passData.bin","ab") as file:
        pickle.dump(passData,file)


print("시작")

GpioManager.init()
GpioManager.setSonic()
SonicManager.onPass = onPass

SonicManager.run()

input("종료하려면 아무 키나 입력")