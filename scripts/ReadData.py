from DataIO import *
import JsonManager
from DataManager import DataManager

#. 데이터 저장을 위한 모듈
dataManager = DataManager()
passDataArr = dataManager.readPassData()

jsonResult = JsonManager.passDataArrayToJson(passDataArr)
print(jsonResult)
for data in passDataArr :
    data.print()