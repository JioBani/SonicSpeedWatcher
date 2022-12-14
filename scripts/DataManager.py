import pickle
import schema.PassData
import os
import JsonManager

#. 데이터 저장 경로
passDataPath = "../static/data/passData.bin"

#. 파일 데이터 입출력을 위한 클래스
class DataManager():

    #. 데이터 저장
    def saveData(self,path,data):
        with open(path,"ab") as file:
            pickle.dump(data,file)
            file.close()

    #. passData 저장
    def savePassData(self,passData):
        self.saveData(path=passDataPath,data=passData)

    #. passData 읽기
    def readPassData(self):
        with open("../static/data/passData.bin", 'rb') as file:
            data = []
            while True:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
                try :
                    passData = pickle.load(file)
                    data.append(passData)
                except EOFError :
                    file.close()
                    return data

    #. passData 초기화
    def resetPassData(self):
      global passDataPath
      msg = input("pass data를 초기화하려면 (y/Y)를 입력해주세요. >> ")
      if(msg == 'y' or msg == 'Y') :
        os.remove(passDataPath)
        f = open(passDataPath,'w')
        f.close()
        print("초기화 완료")

    #. 데이터를 Json형식으로 읽기
    def readByJson(self):
        passDataArr = self.readPassData()
        return JsonManager.passDataArrayToJson(passDataArr)
