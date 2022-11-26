import pickle
import schema.PassData

passDataPath = "../static/data/passData.bin"

class DataManager():

    def saveData(self,path,data):
        with open(path,"ab") as file:
            pickle.dump(data,file)

    def savePassData(self,passData):
        self.saveData(path=passDataPath,data=passData)

    def readPassData(self):
        with open("../static/data/passData.bin", 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기
            passData = pickle.load(file)
            return passData

dataManager = DataManager()
passData = dataManager.readPassData()
print(passData)