from SonicManager import *
from schema.PassData import *
import pickle

def onPass(exitTime, passTime, velocity):
    print("퇴장 시각 : %f" % exitTime)
    print("통과 시간 : %f" % passTime)
    print("평균 속도 : %f" % velocity)

    passData = PassData(
        exitTime=exitTime,
        passingTime=passTime,
        velocity=velocity
    )

    with open("../static/data/passData.bin","ab") as file:
        pickle.dump(passData,file)


GpioManager.init()

sonicManager = SonicManager()
sonicManager.setOnPass(onPass=onPass)
sonicManager.run()