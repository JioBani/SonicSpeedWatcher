function printJsonData(jsonData){

}

function stringToObjectArray(string){
    json = JSON.parse(string);
    var arr = []
    Object.keys(json).forEach((key)=>{
        var passData = {
            'exitTime' : json[key]['exitTime'],
            'passingTime' : json[key]['passingTime'],
            'velocity' : json[key]['velocity'],
            'imagePath' : json[key]['imagePath'],
            'isSpeeding' : json[key]['isSpeeding']
        }
        arr.push(passData)
    })

    arr.forEach((data)=>{
        print(data['exitTime']);
        print(data['passingTime']);
        print(data['velocity']);
        print(data['imagePath']);
        print(data['isSpeeding']);
    })

    return arr;
}