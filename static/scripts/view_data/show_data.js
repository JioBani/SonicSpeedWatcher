//#. view_data.html에서 사용하는 스크립트
//#. 라즈베리 파이에서 받아온 데이터를 테이블로 출력

var passDataArr;

//#. 데이터를 html에 표시하는 함수
function drawData(dataArr) {
    passDataArr = dataArr;
    var i = 0;
    dataArr.forEach((data)=>{
        document.getElementById("show_table_body").innerHTML += getTableItem(data,i);
        i++;
    })

}


//#. passData를 출력하는 table item을 만드는 함수
function getTableItem(passData , i) {
    //#. passData를 바탕으로 tr태그 생성
    var result = `<tr id = ${i}>`;
    result += `<td class="enter_time">${passData['enterTime']}</td>`;
    result += `<td>${passData['exitTime']}</td>`;
    result += `<td>${passData['passingTime']}</td>`;
    result += `<td>${passData['velocity']}km/h</td>`;
    result += `<td style="color : red">${passData['isSpeeding'] == true ? '과속' : '' }</td>`;
    result += `<td></td>`;
    result += `<td style="text-align: center;">
                <button type="button" onclick="onClickShowImage(${i})">
                <img class = "icon" src="../static/web_image/icon_image.svg".svg" width="25px" height="25px">
                </button>
               </td>`;
    result += "</tr>";
    return result;
}


//#. 이미지 보기 버튼을 클릭했을때 실행되는 함수
//#. 이미지 보기 페이지로 이동
function onClickShowImage(index){

    var form = document.createElement('form');

    //#. form 선택된 passData의 정보를 넣어서 전송
    form.setAttribute('method', 'post'); //POST 메서드 적용
    form.setAttribute('action', 'http://192.168.137.42:8080/view_with_image');	// 데이터를 전송할 url

    for (var key in passDataArr[index]) {	// key, value로 이루어진 객체 params
        var hiddenField = document.createElement('input');
        hiddenField.setAttribute('type', 'hidden'); //값 입력
        hiddenField.setAttribute('name', key);
        hiddenField.setAttribute('value', passDataArr[index][key]);
        form.appendChild(hiddenField);
    }
    document.body.appendChild(form);
    form.submit();	// 전송
}