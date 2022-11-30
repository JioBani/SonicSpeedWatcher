var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

var jsonString;
var dataArr;
var chartArr = Array(20);
var speedingArr = Array(20);

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

    // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
    console.log('Subscribing to: ' + topic);
    client.subscribe(topic); // 브로커에 subscribe
}

function publish(topic, msg) {
    if(client == null) return; // 연결되지 않았음
    client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
    if(client == null || isConnected != true) return;
    // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
    console.log('Unsubscribing to: ' + topic);
    client.unsubscribe(topic, null); // 브로커에 subscribe
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
    console.log('오류 : 접속 끊어짐');
    if (responseObject.errorCode !== 0) {
        console.log('<span>오류 : ' + + responseObject.errorMessage);
        //document.getElementById("messages").innerHTML += '<span>오류 : ' + + responseObject.errorMessage + '</span><br/>';
    }
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
  try {
    console.log("onMessageArrived: " + msg.payloadString);

    // 토픽 image가 도착하면 payload에 담긴 파일 이름의 이미지 그리기
    if(msg.destinationName == "image") {
            drawImage(msg.payloadString); // 메시지에 담긴 파일 이름으로 drawImage() 호출. drawImage()는 face.js에 있음
    }

    // 도착한 메시지 출력
    //document.getElementById("messages").innerHTML += '<span>토픽 : ' + msg.destinationName + '  | ' + msg.payloadString + '</span><br/>';
    dataArr = stringToObjectArray(msg.payloadString);

    drawChart();

    var endTime = dataArr[dataArr.length - 1]['enterTime'];
    var speedingNums = 0;
    var speedSum = 0;
    var passTimeSum = 0;
    var velocitySum = 0;

    for(var i = 0; i<20; i++){
      chartArr[i] = 0;
      speedingArr[i] = 0;
    }

    init(endTime);

    dataArr.forEach((data)=>{
      var i = Math.floor((endTime - data['enterTime']) / 60000);
      speedSum += Number(data['velocity']);
      passTimeSum += Number(data['passingTime']);
      velocitySum += Number(data['velocity']);

      if(data['isSpeeding']){
        speedingNums++;
      }

      if(i < 20){
        chartArr[i]++;
        if(data['isSpeeding']){
          speedingArr[i]++;
        }
      }
    })

    chartArr.reverse()
    speedingArr.reverse()

    for(var i = 0; i<20; i++){
      addChartData(0,chartArr[i]);
      addChartData(1,speedingArr[i]);
    }

    document.getElementById('car_numbers').innerHTML = dataArr.length + "대";
    document.getElementById('velocity').innerHTML = (passTimeSum / dataArr.length).toFixed(2) + "초";
    document.getElementById('passing_time').innerHTML = (velocitySum / dataArr.length).toFixed(2) + "km/h";
    document.getElementById('speeding_num').innerHTML = speedingNums + "대";
    document.getElementById('speeding_rate').innerHTML = (speedingNums / dataArr.length * 100).toFixed(2) + "%";


  } catch (error) {
    console.log(error);
  }

}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
  console.log('Disconnected');
}

function requestData(){
    subscribe('json_response');
    publish('json_request' , 'request');
}

function stringToObjectArray(string){
    try {
        console.log(string);
        json = JSON.parse(string);
        var arr = []
        Object.keys(json).forEach((key)=>{
            var enterTime = Math.floor(Number(json[key]['enterTime'] * 1000));
            var exitTime = Math.floor(Number(json[key]['exitTime'] * 1000));

            var passData = {
                'enterTime' : enterTime,
                'exitTime' : exitTime,
                'passingTime' : json[key]['passingTime'].toFixed(2),
                'velocity' : json[key]['velocity'].toFixed(1),
                'imagePath' : json[key]['imagePath'],
                'isSpeeding' : json[key]['isSpeeding']
            }
            arr.push(passData)
        })

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