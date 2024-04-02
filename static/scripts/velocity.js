//#. velocity.html에서 사용하는 스크립트
//#. 전광판 화면 표현

var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

// 접속을 시도하는 함수
function startConnect() {
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

  document.getElementById("messages").innerHTML += '<span>Connected</span><br/>';
}

var topicSave;

function subscribe(topic) {
  if (client == null) return;
  if (isConnected != true) {
    topicSave = topic;
    window.setTimeout("subscribe(topicSave)", 500);
    return
  }

  document.getElementById("messages").innerHTML += '<span>Subscribing to: ' + topic + '</span><br/>';

  client.subscribe(topic);
}

function publish(topic, msg) {
  if (client == null) return;
  client.send(topic, msg, 0, false);
}

function unsubscribe(topic) {
  if (client == null || isConnected != true) return;
  document.getElementById("messages").innerHTML += '<span>Unsubscribing to: ' + topic + '</span><br/>';
  client.unsubscribe(topic, null);
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { /
  document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
  if (responseObject.errorCode !== 0) {
    document.getElementById("messages").innerHTML += '<span>오류 : ' + + responseObject.errorMessage + '</span><br/>';
  }
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) {
  try {
    console.log("onMessageArrived: " + msg.payloadString);

    if (msg.destinationName == "image") {
      drawImage(msg.payloadString);
    }

    arr = msg.payloadString.split('/');

    //#. 속도 출력
    document.getElementById("velocity").innerHTML = Number(arr[0]).toFixed(2).toString() + "km/h";

    //#. 과속 또는 정속 출력
    document.getElementById("speeding").innerHTML = arr[1] + "입니다."

    //#. 과속 또는 정속에 따라 배경색 변경
    if (arr[1] == '정속') {
      document.getElementById('content').style.backgroundColor = '#44F934';
    }
    else {
      document.getElementById('content').style.backgroundColor = '#F46639';
    }
  } catch (error) {
    console.log(error);
  }

}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
  client.disconnect();
  document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
}