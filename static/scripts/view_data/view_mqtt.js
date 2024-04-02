//#. view_data.html에서 사용하는 스크립트
//#. mqtt와 연결

var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

var jsonString;

function startConnect() { // 접속을 시도하는 함수
    clientID = "clientID-" + parseInt(Math.random() * 100);
    broker = ip;
    client = new Paho.MQTT.Client(broker, Number(port), clientID);
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    client.connect({
        onSuccess: onConnect,
    });
}

var isConnected = false;

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
    isConnected = true;
    console.log('Connected')
    requestData();
}

var topicSave;

function subscribe(topic) {
    if(client == null) return;
    if(isConnected != true) {
        topicSave = topic;
        window.setTimeout("subscribe(topicSave)", 500);
        return
    }

    console.log('Subscribing to: ' + topic);
    client.subscribe(topic);
}

function publish(topic, msg) {
    if(client == null) return;
    client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
    if(client == null || isConnected != true) return;
    console.log('Unsubscribing to: ' + topic);
    client.unsubscribe(topic, null);
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) {
    console.log('오류 : 접속 끊어짐');
    if (responseObject.errorCode !== 0) {
        console.log('<span>오류 : ' + + responseObject.errorMessage);
    }
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) {
  console.log("onMessageArrived: " + msg.payloadString);


  if(msg.destinationName == "image") {
          drawImage(msg.payloadString);
  }

  //#. mqtt로 받은 데이터를 Object로 변환 후 html에 그리는 함수로 전송
  drawData(stringToObjectArray(msg.payloadString));
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
  console.log('Disconnected');
}

function requestData(){
    subscribe('json_response');
    publish('json_request' , 'request');
}

//#. mqtt로 받은 문자열을 Json으로 변환 후 Object 배열로 변환
function stringToObjectArray(string){
    try {
        console.log(string);
        json = JSON.parse(string); //#. Json으로 파싱
        var arr = []

        //#. Json을 Object 배열로 변환
        Object.keys(json).forEach((key)=>{
            var enterTime = new Date(Math.floor(Number(json[key]['enterTime'] * 1000)));
            var exitTime = new Date(Math.floor(Number(json[key]['exitTime'] * 1000)));

            var passData = {
                'enterTime' : enterTime.toLocaleString('ko-KR'),
                'exitTime' : exitTime.toLocaleString('ko-KR'),
                'passingTime' : json[key]['passingTime'].toFixed(2),
                'velocity' : json[key]['velocity'].toFixed(1),
                'imagePath' : json[key]['imagePath'],
                'isSpeeding' : json[key]['isSpeeding']
            }
            arr.push(passData)
        })

        //#. 테스트 출력
        arr.forEach((data)=>{
            console.log(data['enterTime']);
            console.log(data['exitTime']);
            console.log(data['passingTime']);
            console.log(data['velocity']);
            console.log(data['imagePath']);
            console.log(data['isSpeeding']);
        })
        return arr;

    } catch (error) {
        console.log(error)
    }

}