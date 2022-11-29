var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음
var ip = "192.168.137.42";

class MqttClient{
    constructor(){
        this.clientId = "clientID-" + parseInt(Math.random() * 100);
        this.client = new Paho.MQTT.Client(broker, Number(port), clientID);
        this.isConnected = false;
        this.topic = "";
    }

    onConnect() {
        isConnected = true;
        document.getElementById("messages").innerHTML += '<span>Connected</span><br/>';
    }

    startConnect() { // 접속을 시도하는 함수
        // client 객체에 콜백 함수 등록
        this.client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
        this.client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록

        // 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}로서, 객체의 프로퍼틴느 onSuccess이고 그 값이 onConnect.
        // 접속에 성공하면 onConnect 함수를 실행하라는 지시
        this.client.connect({
            onSuccess: onConnect,
        });
    }

    subscribe(topic) {
        if(this.client == null) return;
        if(this.isConnected != true) {
            this.topic = topic;
            window.setTimeout("subscribe(topicSave)", 500);
            return
        }

        // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
        document.getElementById("messages").innerHTML += '<span>Subscribing to: ' + topic + '</span><br/>';

        this.client.subscribe(topic); // 브로커에 subscribe
    }

    publish(topic, msg) {
        if(this.client == null) return; // 연결되지 않았음
        this.client.send(topic, msg, 0, false);
    }

    unsubscribe(topic) {
        if(this.client == null || this.isConnected != true) return;

        // 토픽으로 subscribe 하고 있음을 id가 message인 DIV에 출력
        document.getElementById("messages").innerHTML += '<span>Unsubscribing to: ' + topic + '</span><br/>';

        this.client.unsubscribe(topic, null); // 브로커에 subscribe
    }

    onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
        document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
        if (responseObject.errorCode !== 0) {
            document.getElementById("messages").innerHTML += '<span>오류 : ' + + responseObject.errorMessage + '</span><br/>';
        }
    }

    onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
        console.log("onMessageArrived: " + msg.payloadString);

        // 토픽 image가 도착하면 payload에 담긴 파일 이름의 이미지 그리기
        if(msg.destinationName == "image") {
                drawImage(msg.payloadString); // 메시지에 담긴 파일 이름으로 drawImage() 호출. drawImage()는 face.js에 있음
        }

        // 도착한 메시지 출력
        document.getElementById("messages").innerHTML += '<span>토픽 : ' + msg.destinationName + '  | ' + msg.payloadString + '</span><br/>';
        return msg;
    }

    startDisconnect() {
        client.disconnect(); // 브로커에 접속 해제
        document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>';
    }
}