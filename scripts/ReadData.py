from DataIO import *
import JsonManager

dataManager = DataManager()
passDataArr = dataManager.readPassData()

jsonResult = JsonManager.passDataArrayToJson(passDataArr)
print(jsonResult)
for data in passDataArr :
    data.print()