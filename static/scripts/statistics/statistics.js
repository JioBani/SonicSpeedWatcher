var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

var jsonString;
var dataArr;
var chartArr = Array(20);
var speedingArr = Array(20);

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
  try {
    console.log("onMessageArrived: " + msg.payloadString);

    if(msg.destinationName == "image") {
            drawImage(msg.payloadString);
    }

    //#. matt로 받아온 데이터를 Object배열로 변환
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

    //#. 데이터를 순회 하면서 속도 합, 통과 시간 합, 과속 차량 대수 확인
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

    //#. 데이터가 최근일수록 앞으로 정렬되어 있으므로 뒤집기
    chartArr.reverse()
    speedingArr.reverse()

    for(var i = 0; i<20; i++){
      addChartData(0,chartArr[i]);
      addChartData(1,speedingArr[i]);
    }

    //#. 통계 출력
    //#. 통과 차량
    document.getElementById('car_numbers').innerHTML = dataArr.length + "대";

    //#. 평균 통과 시간
    document.getElementById('velocity').innerHTML = (passTimeSum / dataArr.length).toFixed(2) + "초";

    //#. 평균 통과 속도
    document.getElementById('passing_time').innerHTML = (velocitySum / dataArr.length).toFixed(2) + "km/h";

    //#. 과속 차량
    document.getElementById('speeding_num').innerHTML = speedingNums + "대";

    //#. 과속 차량 비율
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


//#. mqtt로 받아온 데이터를 Json으로 변환 후 Object 배열로 변환
function stringToObjectArray(string){
    try {
        console.log(string);
        json = JSON.parse(string); //#. Json으로 변환
        var arr = []

        //#. Object 배열로 변환
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