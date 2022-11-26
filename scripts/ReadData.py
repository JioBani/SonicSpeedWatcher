from DataIO import *

dataManager = DataManager()
passData = dataManager.readPassData()
for data in passData :
    data.print()