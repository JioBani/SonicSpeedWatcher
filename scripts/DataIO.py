import pickle
import schema.PassData

def readData():
    with open("../static/data/passData.bin", 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        passData = pickle.load(file)
        print("퇴장 시각 : %f" % passData.exitTime)
        print("통과 시간 : %f" % passData.passingTime)
        print("평균 속도 : %f" % passData.velocity)

readData()