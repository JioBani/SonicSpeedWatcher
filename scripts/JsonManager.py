import json
import schema.PassData

def dictionaryToJson(dict):
  return json.dumps(dict)

def passDataArrayToJson(arr):
  resultDict = {}
  for passData in arr:
    dict = dictionaryToJson(passData)
    resultDict[dict['exitTime']] = dict
  return json.dumps(resultDict)