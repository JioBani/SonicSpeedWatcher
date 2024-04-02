import json
import schema.PassData

#. 배열 데이터를 Json으로 반환
def passDataArrayToJson(arr):
    #. 배열을 딕셔너리로 변환 후 Json으로 변환
    resultDict = {}
    for passData in arr:
        dict = passData.getDict()
        resultDict[dict['enterTime']] = dict
    return json.dumps(resultDict)