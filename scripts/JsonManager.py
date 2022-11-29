import json
import schema.PassData

def dictionaryToJson(dict):
    return json.dumps(dict)

def passDataArrayToJson(arr):
    resultDict = {}
    for passData in arr:
        dict = passData.getDict()
        resultDict[dict['enterTime']] = dict
    return json.dumps(resultDict)