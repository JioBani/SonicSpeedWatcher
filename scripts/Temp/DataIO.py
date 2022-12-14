import pickle
import schema.PassData

passDataPath = "../static/data/passData.bin"

class DataManager():

    def saveData(self,path,data):
        with open(path,"ab") as file:
            pickle.dump(data,file)
            file.close()

    def savePassData(self,passData):
        self.saveData(path=passDataPath,data=passData)

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