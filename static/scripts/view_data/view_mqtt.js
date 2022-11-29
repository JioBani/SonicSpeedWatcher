var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

var jsonString;

function startConnect() { // 접속을 시도하는 함수
    clientID = "clientID-" + parseInt(Math.random() * 100); // 랜덤한 사용자 ID 생성

    // 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
    broker = ip; // 브로커의 IP 주소
    //broker = "192.168.137.42";
    // id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
    // MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
    client = new Paho.MQTT.Client(broker, Number(port), clientID);

    // client 객체에 콜백 함수 등록
    client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
    client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록

    // 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}로서, 객체의 프로퍼틴느 onSuccess이고 그 값이 onConnect.
    // 접속에 성공하면 onConnect 함수를 실행하라는 지시
    client.connect({
        onSuccess: onConnect,
    });
}

var isConnected = false;

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
    isConnected = true;

    document.getElementById("messages").innerHTML += '<span>Connected</span><br/>';
}

var topicSave;

function subscribe(topic) {
    if(client == null) return;
    if(isConnected != true) {
        topicSave = topic;
        window.setTimeout("subscribe(topicSave)", 500);
        return
    }

    // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
    document.getElementById("messages").innerHTML += '<span>Subscribing to: ' + topic + '</span><br/>';

    client.subscribe(topic); // 브로커에 subscribe
}

function publish(topic, msg) {
    if(client == null) return; // 연결되지 않았음
    client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
    if(client == null || isConnected != true) return;

    // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
    document.getElementById("messages").innerHTML += '<span>Unsubscribing to: ' + topic + '</span><br/>';

    client.unsubscribe(topic, null); // 브로커에 subscribe
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
    document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
    if (responseObject.errorCode !== 0) {
        document.getElementById("messages").innerHTML += '<span>오류 : ' + + responseObject.errorMessage + '</span><br/>';
    }
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
  console.log("onMessageArrived: " + msg.payloadString);

  // 토픽 image가 도착하면 payload에 담긴 파일 이름의 이미지 그리기
  if(msg.destinationName == "image") {
          drawImage(msg.payloadString); // 메시지에 담긴 파일 이름으로 drawImage() 호출. drawImage()는 face.js에 있음
  }

  // 도착한 메시지 출력
  document.getElementById("messages").innerHTML += '<span>토픽 : ' + msg.destinationName + '  | ' + msg.payloadString + '</span><br/>';
  onGetData(stringToObjectArray(msg.payloadString));
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
  client.disconnect(); // 브로커에 접속 해제
  document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}

function requestData(){
    subscribe('json_response');
    publish('json_request' , 'request');
}

function stringToObjectArray(string){
    console.log(string);
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
        console.log(data['exitTime']);
        console.log(data['passingTime']);
        console.log(data['velocity']);
        console.log(data['imagePath']);
        console.log(data['isSpeeding']);

        document.getElementById("show_table_body").innerHTML += getTableTime(data);
    })

    return arr;
}